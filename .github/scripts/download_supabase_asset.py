#!/usr/bin/env python3
"""Stream one private Supabase Storage object to a verified local file."""

from __future__ import annotations

import argparse
import hashlib
import http.client
import os
import sys
import tempfile
from pathlib import Path, PurePosixPath
from urllib.parse import quote, urlsplit, urlunsplit


STREAM_CHUNK_SIZE = 1024 * 1024
MAX_OBJECT_SIZE = 512 * 1024 * 1024


class DownloadError(RuntimeError):
    pass


def fail(message: str) -> "NoReturn":
    raise DownloadError(f"BLOCKED_BINARY_ARTIFACT: {message}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default=os.getenv("SUPABASE_URL"))
    parser.add_argument("--bucket", required=True)
    parser.add_argument("--object", dest="object_path", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--expected-sha256", required=True)
    parser.add_argument("--expected-size", type=int)
    return parser.parse_args()


def validate_object_path(value: str) -> str:
    if not value or value.startswith("/") or "\\" in value or ".." in PurePosixPath(value).parts:
        fail("storage object path must be relative and must not contain '..'")
    if any(ord(char) < 32 for char in value):
        fail("storage object path contains a control character")
    return value


def connection_target(url: str) -> tuple[http.client.HTTPConnection, str]:
    parsed = urlsplit(url)
    if parsed.scheme not in {"https", "http"} or not parsed.netloc:
        fail("Supabase URL must be an absolute http(s) URL")
    connection_type = http.client.HTTPSConnection if parsed.scheme == "https" else http.client.HTTPConnection
    connection = connection_type(parsed.netloc, timeout=120)
    target = urlunsplit(("", "", parsed.path or "/", parsed.query, ""))
    return connection, target


def object_url(base_url: str, bucket: str, object_path: str) -> str:
    if not bucket or any(char not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._-" for char in bucket):
        fail("storage bucket has unsupported characters")
    validate_object_path(object_path)
    return (
        f"{base_url.rstrip('/')}/storage/v1/object/"
        f"{quote(bucket, safe='')}/{quote(object_path, safe='/')}"
    )


def main() -> int:
    args = parse_args()
    temp_path: Path | None = None
    try:
        if not args.base_url:
            fail("SUPABASE_URL is required")
        if len(args.expected_sha256) != 64 or any(
            char not in "0123456789abcdefABCDEF" for char in args.expected_sha256
        ):
            fail("expected SHA-256 must be 64 hexadecimal characters")
        if args.expected_size is not None and args.expected_size <= 0:
            fail("expected size must be positive")

        api_key = os.getenv("SUPABASE_STORAGE_API_KEY")
        auth_token = os.getenv("SUPABASE_STORAGE_AUTH_TOKEN") or api_key
        if not api_key or not auth_token:
            fail(
                "SUPABASE_STORAGE_API_KEY and SUPABASE_STORAGE_AUTH_TOKEN "
                "must be provided as secure environment variables"
            )

        request_url = object_url(args.base_url, args.bucket, args.object_path)
        headers = {
            "apikey": api_key,
            "Authorization": f"Bearer {auth_token}",
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        digest = hashlib.sha256()
        size_bytes = 0
        connection, target = connection_target(request_url)
        try:
            connection.putrequest("GET", target)
            for key, value in headers.items():
                connection.putheader(key, value)
            connection.endheaders()
            response = connection.getresponse()
            if response.status != 200:
                detail = response.read(4096).decode("utf-8", errors="replace").strip()
                fail(f"Storage download failed with HTTP {response.status}: {detail[:240]}")
            declared_size = response.getheader("Content-Length")
            if declared_size and int(declared_size) > MAX_OBJECT_SIZE:
                fail("Storage object exceeds the 512 MiB safety limit")
            with tempfile.NamedTemporaryFile(
                mode="wb", dir=args.output.parent, prefix=f".{args.output.name}.", delete=False
            ) as temp:
                temp_path = Path(temp.name)
                while chunk := response.read(STREAM_CHUNK_SIZE):
                    size_bytes += len(chunk)
                    if size_bytes > MAX_OBJECT_SIZE:
                        fail("Storage object exceeds the 512 MiB safety limit")
                    temp.write(chunk)
                    digest.update(chunk)
        finally:
            connection.close()

        actual_sha256 = digest.hexdigest()
        if args.expected_size is not None and size_bytes != args.expected_size:
            fail(f"size mismatch: expected {args.expected_size}, got {size_bytes}")
        if actual_sha256.lower() != args.expected_sha256.lower():
            fail(
                f"SHA-256 mismatch: expected {args.expected_sha256.lower()}, "
                f"got {actual_sha256}"
            )
        if temp_path is None:
            fail("download did not produce a temporary file")
        os.replace(temp_path, args.output)
        print(f"DOWNLOADED {args.object_path}")
        print(f"SIZE_BYTES {size_bytes}")
        print(f"SHA256 {actual_sha256}")
        return 0
    except DownloadError as exc:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)
        print(str(exc), file=sys.stderr)
        return 2
    except (OSError, ValueError, http.client.HTTPException) as exc:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)
        print(f"BLOCKED_BINARY_ARTIFACT: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
