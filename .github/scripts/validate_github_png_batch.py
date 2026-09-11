#!/usr/bin/env python3
"""Validate a committed GitHub PNG batch and its evidence metadata."""

from __future__ import annotations

import argparse
import hashlib
import json
import struct
from pathlib import Path, PurePosixPath
from typing import Any

MAX_BATCH_FILES = 40
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


class ValidationError(RuntimeError):
    pass


def fail(message: str) -> "NoReturn":
    raise ValidationError(message)


def safe_path(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value:
        fail(f"{field} must be a path")
    if value.startswith(("http://", "https://", "data:", "/")):
        fail(f"{field} must be repository-relative")
    path = PurePosixPath(value)
    if "\\" in value or path.is_absolute() or ".." in path.parts:
        fail(f"{field} contains unsafe traversal")
    normalized = "/".join(part for part in path.parts if part not in {"", "."})
    if not normalized or normalized.lower().endswith(".zip"):
        fail(f"{field} is unsupported")
    return normalized


def digest(path: Path) -> tuple[int, str]:
    size = 0
    checksum = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            size += len(chunk)
            checksum.update(chunk)
    return size, checksum.hexdigest()


def validate_png(path: Path, name: str) -> None:
    with path.open("rb") as stream:
        header = stream.read(26)
    if len(header) < 26 or header[:8] != PNG_SIGNATURE:
        fail(f"{name}: not a PNG")
    ihdr_length = struct.unpack(">I", header[8:12])[0]
    if header[12:16] != b"IHDR" or ihdr_length != 13:
        fail(f"{name}: invalid IHDR")
    width, height = struct.unpack(">II", header[16:24])
    if width <= 0 or height <= 0:
        fail(f"{name}: invalid dimensions {width}x{height}")


def validate(manifest_path: Path, repository_root: Path, expected_repository: str) -> dict[str, Any]:
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"{manifest_path}: cannot read JSON: {exc}")
    if not isinstance(payload, dict):
        fail("manifest root must be an object")
    if payload.get("schema") != "moonveil.github.png_batch":
        fail("wrong batch manifest schema")
    if payload.get("status") not in {"UPLOADED", "PLACED"}:
        fail(f"unsupported batch status: {payload.get('status')!r}")
    if payload.get("repository") != expected_repository:
        fail("manifest repository does not match expected repository")
    asset_root = safe_path(payload.get("asset_root"), "asset_root")
    try:
        batch_index = int(payload["batch_index"])
        total_batches = int(payload["total_batches"])
    except (KeyError, TypeError, ValueError) as exc:
        fail(f"invalid batch numbering: {exc}")
    if batch_index < 1 or total_batches < batch_index:
        fail("invalid batch numbering range")
    records = payload.get("assets")
    if not isinstance(records, list) or not records:
        fail("assets must be a non-empty array")
    if len(records) > MAX_BATCH_FILES:
        fail(f"batch contains {len(records)} files; maximum is {MAX_BATCH_FILES}")
    if payload.get("batch_asset_count") != len(records):
        fail("batch_asset_count does not match assets length")
    seen: set[str] = set()
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            fail(f"assets[{index}] must be an object")
        path = safe_path(record.get("github_path"), f"assets[{index}].github_path")
        if not path.lower().endswith(".png"):
            fail(f"{path}: only PNG files are accepted")
        if not path.startswith(asset_root.rstrip("/") + "/"):
            fail(f"{path}: outside asset_root")
        if path in seen:
            fail(f"duplicate github_path: {path}")
        seen.add(path)
        local = (repository_root / path).resolve()
        if repository_root.resolve() not in local.parents:
            fail(f"{path}: resolved path escaped repository root")
        if not local.is_file():
            fail(f"{path}: committed PNG is missing")
        validate_png(local, path)
        size_bytes, sha256 = digest(local)
        try:
            expected_size = int(record["size_bytes"])
            expected_sha256 = str(record["sha256"]).lower()
        except (KeyError, TypeError, ValueError) as exc:
            fail(f"{path}: missing size_bytes/sha256: {exc}")
        if size_bytes != expected_size:
            fail(f"{path}: size {size_bytes} != {expected_size}")
        if sha256 != expected_sha256:
            fail(f"{path}: SHA-256 mismatch")
        if record.get("content_type") != "image/png":
            fail(f"{path}: content_type must be image/png")
        if payload.get("status") == "PLACED" and record.get("remote_sha256_verified") is not True:
            fail(f"{path}: PLACED requires remote_sha256_verified=true")
    if payload.get("status") == "PLACED":
        commit_sha = payload.get("asset_commit_sha")
        if not isinstance(commit_sha, str) or len(commit_sha) < 7:
            fail("PLACED requires asset_commit_sha")
    return {
        "status": "VERIFIED",
        "manifest": str(manifest_path),
        "batch_index": batch_index,
        "total_batches": total_batches,
        "files": len(records),
        "first_path": records[0]["github_path"],
        "last_path": records[-1]["github_path"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--repository-root", default=".", type=Path)
    parser.add_argument("--expected-repository", default="xxiamadelxx-blip/mac")
    args = parser.parse_args()
    try:
        result = validate(
            args.manifest.resolve(),
            args.repository_root.resolve(),
            args.expected_repository,
        )
    except (ValidationError, OSError) as exc:
        print(f"BLOCKED_BINARY_ARTIFACT: {exc}")
        return 2
    print(
        "VERIFIED "
        f"batch={result['batch_index']}/{result['total_batches']} "
        f"files={result['files']} "
        f"first={result['first_path']} "
        f"last={result['last_path']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
