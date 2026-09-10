#!/usr/bin/env python3
"""Upload a validated Stage 03 ZIP and its text manifest to Supabase Storage.

The archive is always streamed as raw bytes.  The resumable mode uses TUS for
large files; any protocol metadata is text metadata, never a serialization of
the PNG or ZIP bytes.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import http.client
import json
import os
import re
import stat
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import urljoin, urlsplit, urlunsplit, quote
from zipfile import BadZipFile, ZipFile


CHUNK_SIZE = 6 * 1024 * 1024
STREAM_CHUNK_SIZE = 1024 * 1024
MAX_ARCHIVE_SIZE = 512 * 1024 * 1024
ARCHIVE_NAME_RE = re.compile(r"^stage03-assets-[A-Za-z0-9._-]+\.zip$")
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
HERO_IDS = ("lin_yue", "soyeon_han")
DIRECTIONS = (
    "front",
    "back",
    "left",
    "right",
    "north_west",
    "north_east",
    "south_east",
    "south_west",
)
STATES = (
    "idle",
    "move_01",
    "move_02",
    "move_03",
    "attack_01",
    "attack_02",
    "attack_03",
    "hit_01",
    "hit_02",
    "death_01",
    "death_02",
    "shadow",
)


class TransportError(RuntimeError):
    pass


def fail(message: str) -> "NoReturn":
    raise TransportError(f"BLOCKED_BINARY_ARTIFACT: {message}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Stream a validated Stage 03 ZIP to Supabase Storage."
    )
    parser.add_argument("archive", type=Path)
    parser.add_argument("--base-url", default=os.getenv("SUPABASE_URL"))
    parser.add_argument("--bucket", default=os.getenv("SUPABASE_STORAGE_BUCKET", "game-assets"))
    parser.add_argument("--object", dest="object_path")
    parser.add_argument(
        "--mode",
        choices=("auto", "standard", "resumable"),
        default="auto",
        help="auto uses TUS resumable upload above 6 MiB",
    )
    parser.add_argument("--allow-overwrite", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--manifest-output", type=Path)
    parser.add_argument("--checksum-output", type=Path)
    parser.add_argument("--state-file", type=Path)
    return parser.parse_args()


def validate_object_path(value: str) -> str:
    if not value or value.startswith("/") or "\\" in value or ".." in PurePosixPath(value).parts:
        fail("storage object path must be relative and must not contain '..'")
    if any(ord(char) < 32 for char in value):
        fail("storage object path contains a control character")
    return value


def normalize_member(name: str) -> str:
    if "\\" in name or name.startswith("/"):
        fail(f"archive member has an unsafe path: {name!r}")
    prefix = "docs/mockups/03-heroes/"
    if name.startswith(prefix):
        name = name[len(prefix) :]
    if not name or ".." in PurePosixPath(name).parts:
        fail(f"archive member has an unsafe path: {name!r}")
    return name


def validate_png_header(archive: ZipFile, member_name: str) -> None:
    with archive.open(member_name, "r") as stream:
        header = stream.read(26)
    if len(header) < 26 or header[:8] != b"\x89PNG\r\n\x1a\n":
        fail(f"{member_name}: expected a PNG file")
    if header[12:16] != b"IHDR":
        fail(f"{member_name}: PNG IHDR is missing")
    width = int.from_bytes(header[16:20], "big")
    height = int.from_bytes(header[20:24], "big")
    bit_depth = header[24]
    color_type = header[25]
    if (width, height) != (1024, 1024):
        fail(f"{member_name}: expected 1024x1024, got {width}x{height}")
    if bit_depth != 8 or color_type != 6:
        fail(f"{member_name}: expected 8-bit true RGBA PNG")


def inspect_archive(archive_path: Path) -> dict[str, object]:
    if not ARCHIVE_NAME_RE.fullmatch(archive_path.name):
        fail("archive name must match stage03-assets-<id>.zip")
    if not archive_path.is_file():
        fail(f"archive does not exist: {archive_path}")
    size_bytes = archive_path.stat().st_size
    if size_bytes <= 0 or size_bytes > MAX_ARCHIVE_SIZE:
        fail(f"archive size is outside the allowed range: {size_bytes} bytes")

    canonical_names: list[str] = []
    member_pairs: list[tuple[str, str]] = []
    seen: set[str] = set()
    try:
        with ZipFile(archive_path) as archive:
            for info in archive.infolist():
                if info.is_dir():
                    fail(f"archive contains a directory entry: {info.filename}")
                mode = (info.external_attr >> 16) & 0xFFFF
                if stat.S_ISLNK(mode):
                    fail(f"archive contains a symlink: {info.filename}")
                canonical = normalize_member(info.filename)
                if canonical in seen:
                    fail(f"archive contains a duplicate member: {canonical}")
                seen.add(canonical)
                canonical_names.append(canonical)
                member_pairs.append((info.filename, canonical))

            expected_heroes = {name.split("/", 1)[0] for name in canonical_names}
            if not expected_heroes or not expected_heroes.issubset(set(HERO_IDS)):
                fail("archive contains an unknown or missing hero id")
            if len(expected_heroes) > 2:
                fail("archive contains more than two heroes")
            expected = {
                f"{hero}/{direction}/{state}.png"
                for hero in expected_heroes
                for direction in DIRECTIONS
                for state in STATES
            }
            actual = set(canonical_names)
            if actual != expected:
                missing = sorted(expected - actual)
                extra = sorted(actual - expected)
                fail(
                    "archive must contain exactly the complete hero pack; "
                    f"missing={missing[:3]} extra={extra[:3]}"
                )
            for original, _canonical in member_pairs:
                validate_png_header(archive, original)
            bad_member = archive.testzip()
            if bad_member is not None:
                fail(f"archive CRC check failed for {bad_member}")
    except BadZipFile as exc:
        fail(f"invalid ZIP: {exc}")

    digest = hashlib.sha256()
    with archive_path.open("rb") as stream:
        while chunk := stream.read(STREAM_CHUNK_SIZE):
            digest.update(chunk)
    return {
        "size_bytes": size_bytes,
        "sha256": digest.hexdigest(),
        "heroes": sorted(expected_heroes),
        "member_count": len(canonical_names),
    }


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
    connection_type = http.client.HTTPSConnection if parsed.scheme == "https" else http.client.HTTPConnection
    connection = connection_type(parsed.netloc, timeout=120)
    target = urlunsplit(("", "", parsed.path or "/", parsed.query, ""))
    return connection, target


def check_response(response: http.client.HTTPResponse, expected: set[int], operation: str) -> bytes:
    body = response.read(4096)
    if response.status not in expected:
        detail = body.decode("utf-8", errors="replace").strip().replace("\n", " ")
        fail(f"{operation} failed with HTTP {response.status}: {detail[:240]}")
    return body


def object_url(base_url: str, bucket: str, object_path: str) -> str:
    validate_object_path(object_path)
    return (
        f"{base_url.rstrip('/')}/storage/v1/object/"
        f"{quote(bucket, safe='')}/{quote(object_path, safe='/')}"
    )


def upload_raw(
    base_url: str,
    bucket: str,
    object_path: str,
    source: Path,
    content_type: str,
    allow_overwrite: bool,
) -> None:
    url = object_url(base_url, bucket, object_path)
    headers = auth_headers()
    headers.update(
        {
            "Content-Type": content_type,
            "Content-Length": str(source.stat().st_size),
            "x-upsert": "true" if allow_overwrite else "false",
        }
    )
    connection, target = connection_target(url)
    try:
        connection.putrequest("POST", target)
        for key, value in headers.items():
            connection.putheader(key, value)
        connection.endheaders()
        with source.open("rb") as stream:
            while chunk := stream.read(STREAM_CHUNK_SIZE):
                connection.send(chunk)
        response = connection.getresponse()
        check_response(response, {200, 201}, f"raw upload {object_path}")
    except OSError as exc:
        fail(f"raw upload {object_path} was interrupted: {exc}")
    finally:
        connection.close()


def resumable_endpoint(base_url: str) -> str:
    override = os.getenv("SUPABASE_STORAGE_TUS_ENDPOINT")
    if override:
        return override.rstrip("/")
    parsed = urlsplit(base_url)
    host = parsed.hostname or ""
    if host.endswith(".storage.supabase.co"):
        return f"{parsed.scheme}://{parsed.netloc}/storage/v1/upload/resumable"
    match = re.fullmatch(r"([a-z0-9-]+)\.supabase\.co", host)
    if match:
        return f"{parsed.scheme}://{match.group(1)}.storage.supabase.co/storage/v1/upload/resumable"
    fail("TUS needs a Supabase project URL or SUPABASE_STORAGE_TUS_ENDPOINT")


def protocol_metadata(bucket: str, object_path: str, content_type: str) -> str:
    # TUS requires its metadata values to be text-safe.  These values are only
    # bucket/path/content-type metadata; archive bytes never pass through here.
    fields = {
        "bucketName": bucket,
        "objectName": object_path,
        "contentType": content_type,
        "cacheControl": "3600",
    }
    return ",".join(
        f"{key} {base64.b64encode(value.encode('utf-8')).decode('ascii')}"
        for key, value in fields.items()
    )


def create_tus_upload(base_url: str, bucket: str, object_path: str, size_bytes: int, content_type: str, allow_overwrite: bool) -> str:
    endpoint = resumable_endpoint(base_url)
    headers = auth_headers()
    headers.update(
        {
            "Tus-Resumable": "1.0.0",
            "Upload-Length": str(size_bytes),
            "Upload-Metadata": protocol_metadata(bucket, object_path, content_type),
            "x-upsert": "true" if allow_overwrite else "false",
        }
    )
    connection, target = connection_target(endpoint)
    try:
        connection.putrequest("POST", target)
        for key, value in headers.items():
            connection.putheader(key, value)
        connection.endheaders()
        response = connection.getresponse()
        check_response(response, {201}, "create TUS upload")
        location = response.getheader("Location")
        if not location:
            fail("Supabase did not return a TUS upload location")
        return urljoin(endpoint, location)
    finally:
        connection.close()


def tus_offset(location: str) -> int:
    headers = auth_headers()
    headers["Tus-Resumable"] = "1.0.0"
    connection, target = connection_target(location)
    try:
        connection.putrequest("HEAD", target)
        for key, value in headers.items():
            connection.putheader(key, value)
        connection.endheaders()
        response = connection.getresponse()
        check_response(response, {200, 204}, "resume TUS upload")
        raw_offset = response.getheader("Upload-Offset")
        if raw_offset is None:
            fail("Supabase TUS response has no Upload-Offset")
        return int(raw_offset)
    finally:
        connection.close()


def patch_tus_chunk(location: str, source: Path, offset: int, chunk_size: int) -> int:
    headers = auth_headers()
    headers.update(
        {
            "Tus-Resumable": "1.0.0",
            "Upload-Offset": str(offset),
            "Content-Type": "application/offset+octet-stream",
            "Content-Length": str(chunk_size),
        }
    )
    connection, target = connection_target(location)
    try:
        connection.putrequest("PATCH", target)
        for key, value in headers.items():
            connection.putheader(key, value)
        connection.endheaders()
        with source.open("rb") as stream:
            stream.seek(offset)
            remaining = chunk_size
            while remaining:
                chunk = stream.read(min(STREAM_CHUNK_SIZE, remaining))
                if not chunk:
                    fail("archive ended before the declared TUS chunk length")
                connection.send(chunk)
                remaining -= len(chunk)
        response = connection.getresponse()
        check_response(response, {204}, "patch TUS upload")
        raw_offset = response.getheader("Upload-Offset")
        if raw_offset is None:
            fail("Supabase TUS response has no new Upload-Offset")
        return int(raw_offset)
    finally:
        connection.close()


def upload_resumable(
    base_url: str,
    bucket: str,
    object_path: str,
    source: Path,
    content_type: str,
    allow_overwrite: bool,
    state_file: Path,
    sha256: str,
) -> None:
    size_bytes = source.stat().st_size
    location: str | None = None
    offset = 0
    if state_file.exists():
        try:
            state = json.loads(state_file.read_text(encoding="utf-8"))
            if (
                state.get("sha256") == sha256
                and state.get("size_bytes") == size_bytes
                and state.get("bucket") == bucket
                and state.get("object") == object_path
            ):
                location = str(state["location"])
                try:
                    offset = tus_offset(location)
                except (TransportError, ValueError):
                    location = None
                    offset = 0
        except (OSError, json.JSONDecodeError, KeyError, TypeError):
            location = None
            offset = 0

    if location is None:
        location = create_tus_upload(
            base_url,
            bucket,
            object_path,
            size_bytes,
            content_type,
            allow_overwrite,
        )
        state_file.parent.mkdir(parents=True, exist_ok=True)
        state_file.write_text(
            json.dumps(
                {
                    "sha256": sha256,
                    "size_bytes": size_bytes,
                    "bucket": bucket,
                    "object": object_path,
                    "location": location,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    while offset < size_bytes:
        chunk_size = min(CHUNK_SIZE, size_bytes - offset)
        new_offset = patch_tus_chunk(location, source, offset, chunk_size)
        if new_offset != offset + chunk_size:
            fail(f"Supabase returned an unexpected TUS offset: {new_offset}")
        offset = new_offset
        print(f"UPLOADED_BYTES {offset}/{size_bytes}")
    state_file.unlink(missing_ok=True)


def write_text_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> int:
    args = parse_args()
    archive = args.archive.resolve()
    try:
        if not re.fullmatch(r"[A-Za-z0-9._-]+", args.bucket):
            fail("Storage bucket has unsupported characters")
        summary = inspect_archive(archive)
        object_path = validate_object_path(
            args.object_path or f"releases/{archive.name}"
        )
        base_url = args.base_url
        if not base_url and not args.dry_run:
            fail("SUPABASE_URL is required unless --dry-run is used")

        manifest_path = args.manifest_output or archive.with_name(f"{archive.name}.manifest.json")
        checksum_path = args.checksum_output or archive.with_name(f"{archive.name}.sha256")
        manifest_object = f"manifests/{archive.stem}.json"
        checksum_object = f"checksums/{archive.stem}.sha256"
        manifest = {
            "schema": "moonveil.supabase.asset_manifest",
            "schema_version": 1,
            "status": "PENDING_UPLOAD",
            "provider": "supabase_storage",
            "bucket": args.bucket,
            "object": object_path,
            "asset_name": archive.name,
            "content_type": "application/zip",
            "size_bytes": summary["size_bytes"],
            "sha256": summary["sha256"],
            "archive": {
                "format": "zip",
                "heroes": summary["heroes"],
                "member_count": summary["member_count"],
            },
            "manifest_object": manifest_object,
            "checksum_object": checksum_object,
            "runtime_note": "Build-time transport only; the APK contains imported assets and does not require Storage at runtime.",
        }
        write_text_file(manifest_path, json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
        write_text_file(
            checksum_path,
            f"{summary['sha256']}  {archive.name}\n",
        )

        print(f"ARCHIVE {archive}")
        print(f"STORAGE_BUCKET {args.bucket}")
        print(f"STORAGE_OBJECT {object_path}")
        print(f"SIZE_BYTES {summary['size_bytes']}")
        print(f"SHA256 {summary['sha256']}")
        print(f"ZIP_MEMBERS {summary['member_count']}")
        print(f"MANIFEST_FILE {manifest_path}")
        print(f"CHECKSUM_FILE {checksum_path}")

        if args.dry_run:
            print("REMOTE_STATUS PENDING_UPLOAD")
            return 0

        mode = args.mode
        if mode == "auto":
            mode = "resumable" if int(summary["size_bytes"]) > CHUNK_SIZE else "standard"
        if mode == "resumable":
            state_file = args.state_file or archive.with_name(f".{archive.name}.tus.json")
            upload_resumable(
                base_url,
                args.bucket,
                object_path,
                archive,
                "application/zip",
                args.allow_overwrite,
                state_file,
                str(summary["sha256"]),
            )
        else:
            upload_raw(
                base_url,
                args.bucket,
                object_path,
                archive,
                "application/zip",
                args.allow_overwrite,
            )

        manifest["status"] = "UPLOADED"
        write_text_file(manifest_path, json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
        upload_raw(
            base_url,
            args.bucket,
            manifest_object,
            manifest_path,
            "application/json; charset=utf-8",
            args.allow_overwrite,
        )
        upload_raw(
            base_url,
            args.bucket,
            checksum_object,
            checksum_path,
            "text/plain; charset=utf-8",
            args.allow_overwrite,
        )
        print("REMOTE_STATUS UPLOADED")
        return 0
    except TransportError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except (OSError, ValueError, http.client.HTTPException) as exc:
        print(f"BLOCKED_BINARY_ARTIFACT: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
