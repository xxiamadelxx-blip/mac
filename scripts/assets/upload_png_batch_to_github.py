#!/usr/bin/env python3
"""Commit exactly one bounded batch of real PNG files to GitHub.

The script uses GitHub's Git Data API. Base64 is used only inside the HTTP
request for a blob and is never printed into chat, manifests, or reports.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import struct
import sys
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

MAX_BATCH_FILES = 40
MAX_FILE_SIZE = 90 * 1024 * 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
CHUNK_SIZE = 1024 * 1024


class ContractError(RuntimeError):
    pass


class GitHubError(RuntimeError):
    def __init__(self, status: int, detail: str) -> None:
        super().__init__(f"GitHub HTTP {status}: {detail}")
        self.status = status
        self.detail = detail


def api(
    base_url: str,
    token: str,
    method: str,
    endpoint: str,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    body = None
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "User-Agent": "moonveil-github-png-batch-uploader",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if payload is not None:
        body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = Request(
        base_url.rstrip("/") + endpoint,
        data=body,
        headers=headers,
        method=method,
    )
    try:
        with urlopen(request, timeout=120) as response:
            raw = response.read()
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace").strip()
        raise GitHubError(exc.code, detail[:1000]) from exc
    except URLError as exc:
        raise ContractError(f"GitHub request failed: {exc}") from exc
    if not raw:
        return {}
    try:
        value = json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise ContractError(f"GitHub returned non-JSON response: {raw[:200]!r}") from exc
    if not isinstance(value, dict):
        raise ContractError("GitHub response root must be an object")
    return value


def safe_repo_path(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"{field} must be a non-empty repository-relative path")
    if value.startswith(("http://", "https://", "data:", "/")):
        raise ContractError(f"{field} must not be a URL or absolute path: {value!r}")
    path = PurePosixPath(value)
    if "\\" in value or path.is_absolute() or ".." in path.parts:
        raise ContractError(f"{field} contains unsafe traversal: {value!r}")
    normalized = "/".join(part for part in path.parts if part not in {"", "."})
    if not normalized or normalized.lower().endswith(".zip"):
        raise ContractError(f"{field} is unsupported: {value!r}")
    return normalized


def validate_png(path: Path, display_name: str) -> tuple[int, int]:
    try:
        size = path.stat().st_size
    except OSError as exc:
        raise ContractError(f"{display_name}: cannot stat file: {exc}") from exc
    if size <= 0 or size > MAX_FILE_SIZE:
        raise ContractError(f"{display_name}: size {size} is outside 1..{MAX_FILE_SIZE}")
    try:
        with path.open("rb") as stream:
            header = stream.read(26)
    except OSError as exc:
        raise ContractError(f"{display_name}: cannot read file: {exc}") from exc
    if len(header) < 26 or header[:8] != PNG_SIGNATURE:
        raise ContractError(f"{display_name}: file is not a PNG")
    ihdr_length = struct.unpack(">I", header[8:12])[0]
    if header[12:16] != b"IHDR" or ihdr_length != 13:
        raise ContractError(f"{display_name}: missing valid IHDR")
    width, height = struct.unpack(">II", header[16:24])
    if width <= 0 or height <= 0:
        raise ContractError(f"{display_name}: invalid dimensions {width}x{height}")
    return width, height


def digest(path: Path) -> tuple[int, str]:
    size = 0
    checksum = hashlib.sha256()
    try:
        with path.open("rb") as stream:
            while chunk := stream.read(CHUNK_SIZE):
                size += len(chunk)
                checksum.update(chunk)
    except OSError as exc:
        raise ContractError(f"{path}: cannot hash file: {exc}") from exc
    return size, checksum.hexdigest()


def read_manifest(path: Path) -> tuple[str, str, list[dict[str, str]]]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ContractError(f"cannot read source manifest {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ContractError("source manifest root must be an object")
    stage = safe_repo_path(payload.get("stage"), "stage")
    asset_root = safe_repo_path(payload.get("asset_root"), "asset_root")
    raw_assets = payload.get("assets")
    if not isinstance(raw_assets, list) or not raw_assets:
        raise ContractError("source manifest must contain a non-empty assets array")
    records: list[dict[str, str]] = []
    seen: set[str] = set()
    for index, raw in enumerate(raw_assets):
        if not isinstance(raw, dict):
            raise ContractError(f"assets[{index}] must be an object")
        local_path = raw.get("local_path")
        github_path = raw.get("github_path")
        if not isinstance(local_path, str) or not local_path:
            raise ContractError(f"assets[{index}] has no local_path")
        if not isinstance(github_path, str) or not github_path:
            raise ContractError(f"assets[{index}] has no github_path")
        normalized = safe_repo_path(github_path, f"assets[{index}].github_path")
        if not normalized.lower().endswith(".png"):
            raise ContractError(f"{normalized}: only individual PNG files are accepted")
        if not normalized.startswith(asset_root.rstrip("/") + "/"):
            raise ContractError(f"{normalized}: path is outside asset_root {asset_root}")
        if normalized in seen:
            raise ContractError(f"duplicate github_path: {normalized}")
        seen.add(normalized)
        records.append({"local_path": local_path, "github_path": normalized})
    records.sort(key=lambda item: item["github_path"])
    return stage, asset_root, records


def prepare_records(
    source_manifest: Path,
    batch_index: int,
    batch_size: int,
) -> tuple[str, str, list[dict[str, Any]], int]:
    if batch_size != MAX_BATCH_FILES:
        raise ContractError(
            f"batch-size must be exactly {MAX_BATCH_FILES}; only the final remainder may be smaller"
        )
    if batch_index < 1:
        raise ContractError("batch-index must be >= 1")
    stage, asset_root, records = read_manifest(source_manifest)
    total_batches = (len(records) + batch_size - 1) // batch_size
    if batch_index > total_batches:
        raise ContractError(
            f"batch-index {batch_index} is outside 1..{total_batches} for {len(records)} assets"
        )
    start = (batch_index - 1) * batch_size
    selected = records[start : start + batch_size]
    prepared: list[dict[str, Any]] = []
    for record in selected:
        local = Path(record["local_path"]).expanduser()
        if not local.is_file():
            raise ContractError(f"local PNG is missing: {local}")
        width, height = validate_png(local, record["github_path"])
        size_bytes, sha256 = digest(local)
        prepared.append(
            {
                "local_path": str(local),
                "source_file": local.name,
                "github_path": record["github_path"],
                "content_type": "image/png",
                "size_bytes": size_bytes,
                "sha256": sha256,
                "width": width,
                "height": height,
            }
        )
    return stage, asset_root, prepared, total_batches


def branch_state(base_url: str, token: str, repository: str, branch: str) -> tuple[str, str]:
    ref = quote(branch, safe="")
    ref_payload = api(base_url, token, "GET", f"/repos/{repository}/git/ref/heads/{ref}")
    try:
        commit_sha = str(ref_payload["object"]["sha"])
    except (KeyError, TypeError) as exc:
        raise ContractError("GitHub ref response has no commit SHA") from exc
    commit_payload = api(base_url, token, "GET", f"/repos/{repository}/git/commits/{commit_sha}")
    try:
        tree_sha = str(commit_payload["tree"]["sha"])
    except (KeyError, TypeError) as exc:
        raise ContractError("GitHub commit response has no tree SHA") from exc
    return commit_sha, tree_sha


def assert_unoccupied(
    base_url: str,
    token: str,
    repository: str,
    branch: str,
    paths: list[str],
) -> None:
    ref_query = quote(branch, safe="")
    for path in paths:
        encoded_path = quote(path, safe="/")
        try:
            api(
                base_url,
                token,
                "GET",
                f"/repos/{repository}/contents/{encoded_path}?ref={ref_query}",
            )
        except GitHubError as exc:
            if exc.status == 404:
                continue
            raise
        raise ContractError(f"refusing to overwrite existing GitHub path: {path}")


def create_blob(base_url: str, token: str, repository: str, path: Path) -> str:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise ContractError(f"{path}: cannot read for upload: {exc}") from exc
    response = api(
        base_url,
        token,
        "POST",
        f"/repos/{repository}/git/blobs",
        {"encoding": "base64", "content": base64.b64encode(raw).decode("ascii")},
    )
    sha = response.get("sha")
    if not isinstance(sha, str) or not sha:
        raise ContractError(f"GitHub did not return a blob SHA for {path}")
    return sha


def create_text_blob(
    base_url: str,
    token: str,
    repository: str,
    content: str,
) -> str:
    response = api(
        base_url,
        token,
        "POST",
        f"/repos/{repository}/git/blobs",
        {"encoding": "utf-8", "content": content},
    )
    sha = response.get("sha")
    if not isinstance(sha, str) or not sha:
        raise ContractError("GitHub did not return a text blob SHA")
    return sha


def create_tree(
    base_url: str,
    token: str,
    repository: str,
    base_tree: str,
    entries: list[dict[str, str]],
) -> str:
    response = api(
        base_url,
        token,
        "POST",
        f"/repos/{repository}/git/trees",
        {"base_tree": base_tree, "tree": entries},
    )
    sha = response.get("sha")
    if not isinstance(sha, str) or not sha:
        raise ContractError("GitHub did not return a tree SHA")
    return sha


def create_commit(
    base_url: str,
    token: str,
    repository: str,
    message: str,
    parent: str,
    tree: str,
) -> str:
    response = api(
        base_url,
        token,
        "POST",
        f"/repos/{repository}/git/commits",
        {"message": message, "parents": [parent], "tree": tree},
    )
    sha = response.get("sha")
    if not isinstance(sha, str) or not sha:
        raise ContractError("GitHub did not return a commit SHA")
    return sha


def move_branch(
    base_url: str,
    token: str,
    repository: str,
    branch: str,
    expected_parent: str,
    commit_sha: str,
) -> None:
    current, _ = branch_state(base_url, token, repository, branch)
    if current != expected_parent:
        raise ContractError(
            f"branch moved during batch: expected {expected_parent}, found {current}; no force update"
        )
    ref = quote(branch, safe="")
    api(
        base_url,
        token,
        "PATCH",
        f"/repos/{repository}/git/refs/heads/{ref}",
        {"sha": commit_sha, "force": False},
    )


def verify_remote_blob(
    base_url: str,
    token: str,
    repository: str,
    blob_sha: str,
    expected_size: int,
    expected_sha256: str,
) -> None:
    response = api(base_url, token, "GET", f"/repos/{repository}/git/blobs/{blob_sha}")
    if response.get("encoding") != "base64" or not isinstance(response.get("content"), str):
        raise ContractError(f"GitHub blob {blob_sha} is not a base64 blob response")
    try:
        raw = base64.b64decode(response["content"], validate=False)
    except (ValueError, TypeError) as exc:
        raise ContractError(f"cannot decode GitHub blob {blob_sha}") from exc
    actual_sha256 = hashlib.sha256(raw).hexdigest()
    if len(raw) != expected_size or actual_sha256 != expected_sha256:
        raise ContractError(
            f"remote blob {blob_sha} mismatch: "
            f"size {len(raw)} != {expected_size} or SHA-256 {actual_sha256} != {expected_sha256}"
        )


def evidence_path(stage: str, batch_index: int) -> str:
    return f"docs/asset_batches/{stage}/batch-{batch_index:03d}.json"


def report_payload(
    *,
    status: str,
    repository: str,
    branch: str,
    stage: str,
    source_manifest: Path,
    batch_index: int,
    total_batches: int,
    records: list[dict[str, Any]],
    evidence: str,
    asset_commit_sha: str | None = None,
    evidence_commit_sha: str | None = None,
    error: str | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "schema": "moonveil.github.png_batch_report",
        "version": 1,
        "status": status,
        "repository": repository,
        "branch": branch,
        "stage": stage,
        "batch_index": batch_index,
        "total_batches": total_batches,
        "batch_asset_count": len(records),
        "source_manifest": str(source_manifest),
        "evidence_path": evidence,
        "first_github_path": records[0]["github_path"] if records else None,
        "last_github_path": records[-1]["github_path"] if records else None,
        "assets": [
            {
                "github_path": item["github_path"],
                "source_file": item["source_file"],
                "size_bytes": item["size_bytes"],
                "sha256": item["sha256"],
                "git_blob_sha": item.get("git_blob_sha"),
                "remote_sha256_verified": item.get("remote_sha256_verified", False),
            }
            for item in records
        ],
    }
    if asset_commit_sha:
        payload["asset_commit_sha"] = asset_commit_sha
        payload["asset_commit_url"] = f"https://github.com/{repository}/commit/{asset_commit_sha}"
    if evidence_commit_sha:
        payload["evidence_commit_sha"] = evidence_commit_sha
        payload["evidence_commit_url"] = f"https://github.com/{repository}/commit/{evidence_commit_sha}"
    if status == "PLACED":
        next_index = batch_index + 1
        payload["next_action"] = (
            f"Start a separate agent run for batch {next_index} of {total_batches}; reread live main and verify this evidence first."
            if next_index <= total_batches
            else "All batches are placed; do not upload another batch."
        )
    elif status == "DRY_RUN":
        payload["next_action"] = "Run this same batch with an authorized GitHub token."
    elif status == "PARTIAL_GITHUB_BATCH":
        payload["next_action"] = "Inspect the asset commit and complete or reconcile this batch before starting another."
    else:
        payload["next_action"] = "Restore the missing capability, then rerun only this batch."
    if error:
        payload["error"] = error
    return payload


def emit_report(report: dict[str, Any], output_path: Path | None) -> None:
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if output_path is not None:
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")
        except OSError as exc:
            raise ContractError(f"cannot write report {output_path}: {exc}") from exc
    print(rendered, end="")


def run(args: argparse.Namespace) -> dict[str, Any]:
    source_manifest = Path(args.source_manifest).expanduser().resolve()
    stage, asset_root, records, total_batches = prepare_records(
        source_manifest, args.batch_index, args.batch_size
    )
    evidence = evidence_path(stage, args.batch_index)
    common = {
        "repository": args.repository,
        "branch": args.branch,
        "stage": stage,
        "source_manifest": source_manifest,
        "batch_index": args.batch_index,
        "total_batches": total_batches,
        "records": records,
        "evidence": evidence,
    }
    if args.dry_run:
        return report_payload(status="DRY_RUN", **common)

    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if not token:
        raise ContractError("GITHUB_TOKEN or GH_TOKEN is required; use --dry-run for local checks")
    base_url = os.getenv("GITHUB_API_URL", "https://api.github.com")
    parent_sha, parent_tree = branch_state(base_url, token, args.repository, args.branch)
    assert_unoccupied(
        base_url,
        token,
        args.repository,
        args.branch,
        [item["github_path"] for item in records] + [evidence],
    )

    asset_blob_entries: list[dict[str, str]] = []
    for item in records:
        blob_sha = create_blob(base_url, token, args.repository, Path(item["local_path"]))
        item["git_blob_sha"] = blob_sha
        asset_blob_entries.append(
            {"path": item["github_path"], "mode": "100644", "type": "blob", "sha": blob_sha}
        )

    provisional = {
        "schema": "moonveil.github.png_batch",
        "version": 1,
        "status": "UPLOADED",
        "repository": args.repository,
        "branch": args.branch,
        "stage": stage,
        "asset_root": asset_root,
        "batch_index": args.batch_index,
        "total_batches": total_batches,
        "batch_asset_count": len(records),
        "batching": {
            "max_files_per_batch": MAX_BATCH_FILES,
            "one_batch_per_agent_run": True,
        },
        "assets": [
            {
                "github_path": item["github_path"],
                "source_file": item["source_file"],
                "content_type": item["content_type"],
                "size_bytes": item["size_bytes"],
                "sha256": item["sha256"],
                "git_blob_sha": item["git_blob_sha"],
            }
            for item in records
        ],
        "asset_commit_sha": None,
        "next_action": "Verify every GitHub blob before changing this evidence to PLACED.",
    }
    provisional_blob = create_text_blob(
        base_url,
        token,
        args.repository,
        json.dumps(provisional, ensure_ascii=False, indent=2) + "\n",
    )
    upload_tree = create_tree(
        base_url,
        token,
        args.repository,
        parent_tree,
        asset_blob_entries
        + [{"path": evidence, "mode": "100644", "type": "blob", "sha": provisional_blob}],
    )
    asset_commit_sha = create_commit(
        base_url,
        token,
        args.repository,
        f"Assets: upload GitHub PNG batch {args.batch_index:03d}/{total_batches:03d} ({len(records)} files)",
        parent_sha,
        upload_tree,
    )
    move_branch(base_url, token, args.repository, args.branch, parent_sha, asset_commit_sha)

    for item in records:
        verify_remote_blob(
            base_url,
            token,
            args.repository,
            item["git_blob_sha"],
            item["size_bytes"],
            item["sha256"],
        )
        item["remote_sha256_verified"] = True

    current_sha, asset_tree = branch_state(base_url, token, args.repository, args.branch)
    if current_sha != asset_commit_sha:
        raise ContractError(
            f"branch moved after asset commit: expected {asset_commit_sha}, found {current_sha}"
        )
    final = {
        **provisional,
        "status": "PLACED",
        "asset_commit_sha": asset_commit_sha,
        "asset_commit_url": f"https://github.com/{args.repository}/commit/{asset_commit_sha}",
        "verified_at": datetime.now(timezone.utc).isoformat(),
        "assets": [
            {
                "github_path": item["github_path"],
                "source_file": item["source_file"],
                "content_type": item["content_type"],
                "size_bytes": item["size_bytes"],
                "sha256": item["sha256"],
                "git_blob_sha": item["git_blob_sha"],
                "remote_sha256_verified": True,
            }
            for item in records
        ],
    }
    final_blob = create_text_blob(
        base_url,
        token,
        args.repository,
        json.dumps(final, ensure_ascii=False, indent=2) + "\n",
    )
    final_tree = create_tree(
        base_url,
        token,
        args.repository,
        asset_tree,
        [{"path": evidence, "mode": "100644", "type": "blob", "sha": final_blob}],
    )
    evidence_commit_sha = create_commit(
        base_url,
        token,
        args.repository,
        f"Evidence: place GitHub PNG batch {args.batch_index:03d}/{total_batches:03d}",
        asset_commit_sha,
        final_tree,
    )
    move_branch(
        base_url,
        token,
        args.repository,
        args.branch,
        asset_commit_sha,
        evidence_commit_sha,
    )
    return report_payload(
        status="PLACED",
        asset_commit_sha=asset_commit_sha,
        evidence_commit_sha=evidence_commit_sha,
        **common,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", default=os.getenv("GITHUB_REPOSITORY"))
    parser.add_argument("--branch", default="main")
    parser.add_argument("--source-manifest", required=True)
    parser.add_argument("--batch-index", required=True, type=int)
    parser.add_argument("--batch-size", type=int, default=MAX_BATCH_FILES)
    parser.add_argument("--report-output")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if not args.repository:
        parser.error("--repository or GITHUB_REPOSITORY is required")
    if "/" not in args.repository:
        parser.error("--repository must be owner/name")
    output = Path(args.report_output).expanduser().resolve() if args.report_output else None
    try:
        report = run(args)
        emit_report(report, output)
        return 0 if report["status"] in {"PLACED", "DRY_RUN"} else 2
    except (ContractError, GitHubError) as exc:
        report = {
            "schema": "moonveil.github.png_batch_report",
            "version": 1,
            "status": "BLOCKED_BINARY_ARTIFACT",
            "repository": args.repository,
            "branch": args.branch,
            "batch_index": args.batch_index,
            "error": str(exc),
            "next_action": "Restore the missing capability, then rerun only this batch.",
        }
        emit_report(report, output)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
