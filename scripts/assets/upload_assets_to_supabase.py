#!/usr/bin/env python3
"""Upload individual visual assets to Supabase Storage.

The manifest lists one local file and one Storage object per asset.  Bytes are
streamed directly to Storage; the manifest and upload report contain metadata
only.  This tool never creates or accepts an archive.
"""

from __future__ import annotations

import argparse
import hashlib
import http.client
import json
import mimetypes
import os
import sys
import time
from pathlib import Path, PurePosixPath
from urllib.parse import quote, urlsplit, urlunsplit


STREAM_CHUNK_SIZE = 1024 * 1024
MAX_FILE_SIZE = 512 * 1024 * 1024
RETRY_COUNT = 3


class TransportError(RuntimeError):
    pass


def fail(message: str) -> "NoReturn":
    raise TransportError(f"BLOCKED_BINARY_ARTIFACT: {message}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--base-url", default=os.getenv("SUPABASE_URL"))
    parser.add_argument(
        "--bucket",
        default=os.getenv("SUPABASE_STORAGE_BUCKET", "visual-assets"),
    )
    parser.add_argument("--allow-overwrite", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--report-output", type=Path)
    return parser.parse_args()


def validate_bucket(value: str) -> str:
    if not value or any(
        char not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._-"
        for char in value
    ):
        fail("Storage bucket has unsupported characters")
    return value


def validate_object_path(value: str) -> str:
    if (
        not value
        or value.startswith("/")
        or "\\" in value
        or ".." in PurePosixPath(value).parts
    ):
        fail("Storage object path must be relative and must not contain '..'")
    if any(ord(char) < 32 for char in value):
        fail("Storage object path contains a control character")
    if value.lower().endswith(".zip"):
        fail("archive objects are not accepted; list individual visual files")
    return value


def resolve_local_path(manifest_path: Path, value: str) -> Path:
    if not value or Path(value).is_absolute():
        fail(f"local_path must be a relative path: {value!r}")
    if ".." in PurePosixPath(value).parts or "\\" in value:
        fail(f"local_path is unsafe: {value!r}")
    root = manifest_path.parent.resolve()
    resolved = (root / value).resolve()
    if root != resolved and root not in resolved.parents:
        fail(f"local_path escapes the manifest directory: {value!r}")
    if resolved.suffix.lower() == ".zip":
        fail("archive inputs are not accepted; upload individual visual files")
    return resolved


def content_type_for(record: dict[str, object], local_path: Path) -> str:
    declared = record.get("content_type")
    content_type = str(declared) if declared else mimetypes.guess_type(local_path.name)[0]
    if not content_type:
        fail(f"cannot infer content type for {local_path.name}")
    if content_type == "application/zip" or local_path.suffix.lower() == ".zip":
        fail("archive content is not accepted")
    if content_type not in {"image/png", "image/svg+xml"}:
        fail(f"unsupported visual content type for {local_path.name}: {content_type}")
    return content_type


def file_digest(path: Path) -> tuple[int, str]:
    if not path.is_file():
        fail(f"local asset does not exist: {path}")
    size_bytes = path.stat().st_size
    if size_bytes <= 0 or size_bytes > MAX_FILE_SIZE:
        fail(f"asset size is outside the allowed range: {path}")
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(STREAM_CHUNK_SIZE):
            digest.update(chunk)
    return size_bytes, digest.hexdigest()


def inspect_manifest(manifest_path: Path, bucket: str) -> list[dict[str, object]]:
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read manifest: {exc}")
    if not isinstance(payload, dict):
        fail("manifest root must be an object")
    records = payload.get("assets")
    if not isinstance(records, list) or not records:
        fail("manifest must contain a non-empty assets array")

    seen_objects: set[str] = set()
    seen_local_paths: set[str] = set()
    inspected: list[dict[str, object]] = []
    for index, raw_record in enumerate(records):
        if not isinstance(raw_record, dict):
            fail(f"assets[{index}] must be an object")
        local_value = raw_record.get("local_path")
        object_value = raw_record.get("object")
        if not isinstance(local_value, str) or not isinstance(object_value, str):
            fail(f"assets[{index}] requires local_path and object")
        object_path = validate_object_path(object_value)
        if object_path in seen_objects:
            fail(f"duplicate Storage object: {object_path}")
        seen_objects.add(object_path)
        local_path = resolve_local_path(manifest_path, local_value)
        local_key = local_path.as_posix()
        if local_key in seen_local_paths:
            fail(f"duplicate local asset: {local_value}")
        seen_local_paths.add(local_key)
        content_type = content_type_for(raw_record, local_path)
        size_bytes, sha256 = file_digest(local_path)

        declared_size = raw_record.get("size_bytes")
        if declared_size is not None and int(declared_size) != size_bytes:
            fail(
                f"{local_value}: size mismatch; manifest={declared_size}, "
                f"actual={size_bytes}"
            )
        declared_sha256 = raw_record.get("sha256")
        if declared_sha256 is not None and str(declared_sha256).lower() != sha256:
            fail(
                f"{local_value}: SHA-256 mismatch; manifest={declared_sha256}, "
                f"actual={sha256}"
            )

        inspected.append(
            {
                "local_path": local_value,
                "object": object_path,
                "content_type": content_type,
                "size_bytes": size_bytes,
                "sha256": sha256,
            }
        )
    return inspected


def auth_headers() -> dict[str, str]:
    api_key = os.getenv("SUPABASE_STORAGE_API_KEY")
    auth_token = os.getenv("SUPABASE_STORAGE_AUTH_TOKEN") or api_key
    if not api_key or not auth_token:
        fail(
            "SUPABASE_STORAGE_API_KEY and SUPABASE_STORAGE_AUTH_TOKEN "
            "must be provided as secure environment variables"
        )
    return {"apikey": api_key, "Authorization": f"Bearer {auth_token}"}


def connection_target(url: str) -> tuple[http.client.HTTPConnection, str]:
    parsed = urlsplit(url)
    if parsed.scheme not in {"https", "http"} or not parsed.netloc:
        fail("Supabase URL must be an absolute http(s) URL")
    connection_type = (
        http.client.HTTPSConnection
        if parsed.scheme == "https"
        else http.client.HTTPConnection
    )
    connection = connection_type(parsed.netloc, timeout=120)
    target = urlunsplit(("", "", parsed.path or "/", parsed.query, ""))
    return connection, target


def object_url(base_url: str, bucket: str, object_path: str) -> str:
    return (
        f"{base_url.rstrip('/')}/storage/v1/object/"
        f"{quote(bucket, safe='')}/{quote(object_path, safe='/')}"
    )


def response_detail(response: http.client.HTTPResponse) -> str:
    return response.read(4096).decode("utf-8", errors="replace").strip().replace(
        "\n", " "
    )[:240]


def upload_raw(
    base_url: str,
    bucket: str,
    record: dict[str, object],
    manifest_path: Path,
    allow_overwrite: bool,
) -> None:
    source = resolve_local_path(manifest_path, str(record["local_path"]))
    url = object_url(base_url, bucket, str(record["object"]))
    for attempt in range(1, RETRY_COUNT + 1):
        connection: http.client.HTTPConnection | None = None
        try:
            headers = auth_headers()
            headers.update(
                {
                    "Content-Type": str(record["content_type"]),
                    "Content-Length": str(record["size_bytes"]),
                    "x-upsert": "true" if allow_overwrite else "false",
                }
            )
            connection, target = connection_target(url)
            connection.putrequest("POST", target)
            for key, value in headers.items():
                connection.putheader(key, value)
            connection.endheaders()
            with source.open("rb") as stream:
                while chunk := stream.read(STREAM_CHUNK_SIZE):
                    connection.send(chunk)
            response = connection.getresponse()
            if response.status in {200, 201}:
                response.read(4096)
                return
            detail = response_detail(response)
            if response.status in {400, 401, 403, 409}:
                fail(
                    f"upload {record['object']} failed with HTTP "
                    f"{response.status}: {detail}"
                )
            if attempt == RETRY_COUNT:
                fail(
                    f"upload {record['object']} failed with HTTP "
                    f"{response.status}: {detail}"
                )
        except (OSError, http.client.HTTPException) as exc:
            if attempt == RETRY_COUNT:
                fail(f"upload {record['object']} was interrupted: {exc}")
            time.sleep(attempt)
        finally:
            if connection is not None:
                connection.close()


def verify_remote(
    base_url: str,
    bucket: str,
    record: dict[str, object],
) -> None:
    headers = auth_headers()
    connection, target = connection_target(
        object_url(base_url, bucket, str(record["object"]))
    )
    digest = hashlib.sha256()
    size_bytes = 0
    try:
        connection.putrequest("GET", target)
        for key, value in headers.items():
            connection.putheader(key, value)
        connection.endheaders()
        response = connection.getresponse()
        if response.status != 200:
            fail(
                f"verification of {record['object']} failed with HTTP "
                f"{response.status}: {response_detail(response)}"
            )
        while chunk := response.read(STREAM_CHUNK_SIZE):
            size_bytes += len(chunk)
            if size_bytes > MAX_FILE_SIZE:
                fail(f"remote object is too large: {record['object']}")
            digest.update(chunk)
    except (OSError, http.client.HTTPException) as exc:
        fail(f"verification of {record['object']} was interrupted: {exc}")
    finally:
        connection.close()

    actual_sha256 = digest.hexdigest()
    if size_bytes != int(record["size_bytes"]):
        fail(
            f"remote size mismatch for {record['object']}: "
            f"expected {record['size_bytes']}, got {size_bytes}"
        )
    if actual_sha256 != str(record["sha256"]):
        fail(
            f"remote SHA-256 mismatch for {record['object']}: "
            f"expected {record['sha256']}, got {actual_sha256}"
        )


def main() -> int:
    args = parse_args()
    manifest_path = args.manifest.resolve()
    try:
        bucket = validate_bucket(args.bucket)
        records = inspect_manifest(manifest_path, bucket)
        if not args.dry_run and not args.base_url:
            fail("SUPABASE_URL is required unless --dry-run is used")

        report: dict[str, object] = {
            "schema": "moonveil.supabase.asset_upload_report",
            "version": 1,
            "status": "DRY_RUN" if args.dry_run else "PENDING",
            "provider": "supabase_storage",
            "bucket": bucket,
            "assets": records,
        }
        for record in records:
            print(
                f"ASSET {record['object']} "
                f"SIZE_BYTES={record['size_bytes']} SHA256={record['sha256']}"
            )

        if not args.dry_run:
            for record in records:
                upload_raw(
                    args.base_url,
                    bucket,
                    record,
                    manifest_path,
                    args.allow_overwrite,
                )
                verify_remote(args.base_url, bucket, record)
                print(f"VERIFIED {record['object']}")
            report["status"] = "VERIFIED"

        if args.report_output:
            args.report_output.parent.mkdir(parents=True, exist_ok=True)
            args.report_output.write_text(
                json.dumps(report, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
        print(f"REMOTE_STATUS {report['status']}")
        return 0
    except (TransportError, OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
