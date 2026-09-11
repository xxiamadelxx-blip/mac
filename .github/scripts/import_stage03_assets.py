#!/usr/bin/env python3
"""Validate and stage individual Stage 03 hero PNGs for a build workspace."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import struct
import sys
import tempfile
from pathlib import Path, PurePosixPath


HEROES = {"lin_yue", "soyeon_han"}
DIRECTIONS = {
    "front",
    "back",
    "left",
    "right",
    "north_west",
    "north_east",
    "south_east",
    "south_west",
}
STATES = {
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
}
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
STREAM_CHUNK_SIZE = 1024 * 1024
MAX_FILE_SIZE = 32 * 1024 * 1024


def fail(message: str) -> "NoReturn":
    raise SystemExit(f"ERROR: {message}")


def safe_relative(value: str) -> str:
    path = PurePosixPath(value)
    if (
        not value
        or path.is_absolute()
        or ".." in path.parts
        or "\\" in value
        or value.lower().endswith(".zip")
    ):
        fail(f"unsafe or unsupported asset path: {value!r}")
    return "/".join(part for part in path.parts if part not in {"", "."})


def load_manifest(path: Path) -> list[dict[str, object]]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read request manifest: {exc}")
    if not isinstance(payload, dict):
        fail("request manifest root must be an object")
    if payload.get("status") != "READY":
        fail(f"request status is {payload.get('status')!r}, expected READY")
    records = payload.get("assets")
    if not isinstance(records, list) or not records:
        fail("request manifest must contain a non-empty assets array")
    result: list[dict[str, object]] = []
    seen: set[str] = set()
    for index, raw in enumerate(records):
        if not isinstance(raw, dict):
            fail(f"assets[{index}] must be an object")
        local_path = raw.get("local_path")
        if not isinstance(local_path, str):
            fail(f"assets[{index}] has no local_path")
        normalized = safe_relative(local_path)
        if normalized in seen:
            fail(f"duplicate local_path: {normalized}")
        seen.add(normalized)
        result.append({**raw, "local_path": normalized})
    return result


def expected_for(hero: str) -> set[str]:
    return {
        f"{hero}/{direction}/{state}.png"
        for direction in sorted(DIRECTIONS)
        for state in sorted(STATES)
    }


def validate_png(path: Path, display_name: str) -> None:
    if path.stat().st_size <= 0 or path.stat().st_size > MAX_FILE_SIZE:
        fail(f"{display_name}: file size is outside the allowed range")
    with path.open("rb") as stream:
        header = stream.read(26)
    if len(header) < 26 or header[:8] != PNG_SIGNATURE:
        fail(f"{display_name}: not a PNG file")
    ihdr_length = struct.unpack(">I", header[8:12])[0]
    if header[12:16] != b"IHDR" or ihdr_length != 13:
        fail(f"{display_name}: missing or invalid PNG IHDR")
    width, height, bit_depth, color_type = struct.unpack(">IIBB", header[16:26])
    if (width, height) != (1024, 1024):
        fail(f"{display_name}: expected 1024x1024, got {width}x{height}")
    if bit_depth != 8 or color_type != 6:
        fail(
            f"{display_name}: expected 8-bit true RGBA PNG, "
            f"got bit_depth={bit_depth}, color_type={color_type}"
        )


def digest(path: Path) -> tuple[int, str]:
    size_bytes = 0
    sha256 = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(STREAM_CHUNK_SIZE):
            size_bytes += len(chunk)
            sha256.update(chunk)
    return size_bytes, sha256.hexdigest()


def main() -> int:
    if len(sys.argv) not in (3, 4):
        fail(
            "usage: import_stage03_assets.py REQUEST.json DOWNLOAD_ROOT "
            "[TARGET_ROOT]"
        )
    request_path = Path(sys.argv[1]).resolve()
    download_root = Path(sys.argv[2]).resolve()
    target_root = Path(
        sys.argv[3] if len(sys.argv) == 4 else "build_assets/docs/mockups/03-heroes"
    ).resolve()
    if not download_root.is_dir():
        fail(f"download root does not exist: {download_root}")

    records = load_manifest(request_path)
    entries: dict[str, tuple[Path, dict[str, object]]] = {}
    for record in records:
        local_path = str(record["local_path"])
        source = (download_root / local_path).resolve()
        if download_root not in source.parents:
            fail(f"resolved source escaped download root: {local_path}")
        if not source.is_file():
            fail(f"downloaded asset is missing: {local_path}")
        if not local_path.endswith(".png"):
            fail(f"Stage 03 hero asset must be PNG: {local_path}")
        parts = local_path.split("/")
        if len(parts) != 3 or parts[0] not in HEROES:
            fail(f"unsupported hero asset path: {local_path}")
        hero, direction, state_file = parts
        state = state_file.removesuffix(".png")
        if direction not in DIRECTIONS or state not in STATES:
            fail(f"unsupported direction/state: {local_path}")
        validate_png(source, local_path)
        size_bytes, sha256 = digest(source)
        expected_size = record.get("size_bytes")
        expected_sha256 = record.get("sha256")
        if expected_size is None or expected_sha256 is None:
            fail(f"{local_path}: request lacks size_bytes or sha256")
        if int(expected_size) != size_bytes:
            fail(f"{local_path}: size mismatch")
        if str(expected_sha256).lower() != sha256:
            fail(f"{local_path}: SHA-256 mismatch")
        if local_path in entries:
            fail(f"duplicate hero asset: {local_path}")
        entries[local_path] = (source, record)

    heroes_present = {path.split("/", 1)[0] for path in entries}
    for hero in sorted(heroes_present):
        actual = {path for path in entries if path.startswith(f"{hero}/")}
        expected = expected_for(hero)
        if actual != expected:
            missing = sorted(expected - actual)
            extra = sorted(actual - expected)
            fail(
                f"{hero} is incomplete; missing={missing[:8]} "
                f"extra={extra[:8]}"
            )

    target_root.mkdir(parents=True, exist_ok=True)
    temporary_root = Path(
        tempfile.mkdtemp(prefix=".stage03-assets-", dir=str(target_root.parent))
    )
    try:
        destinations: dict[str, Path] = {}
        for local_path, (source, _record) in sorted(entries.items()):
            destination = (target_root / local_path).resolve()
            if target_root not in destination.parents:
                fail(f"resolved destination escaped target root: {local_path}")
            if destination.exists():
                existing_size, existing_sha256 = digest(destination)
                source_size, source_sha256 = digest(source)
                if (existing_size, existing_sha256) != (source_size, source_sha256):
                    fail(f"refusing to replace a different existing asset: {destination}")
                continue
            staged = temporary_root / local_path
            staged.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, staged)
            destinations[local_path] = destination

        for local_path, destination in destinations.items():
            destination.parent.mkdir(parents=True, exist_ok=True)
            os.replace(temporary_root / local_path, destination)
    finally:
        shutil.rmtree(temporary_root, ignore_errors=True)

    for local_path in sorted(entries):
        print(f"STAGED {target_root / local_path}")
    print(f"SUMMARY heroes={','.join(sorted(heroes_present))} files={len(entries)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
