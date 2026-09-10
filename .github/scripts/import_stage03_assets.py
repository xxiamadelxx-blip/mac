#!/usr/bin/env python3
"""Validate and atomically import a Stage 03 hero PNG archive.

The archive is deliberately handled as bytes by the GitHub Actions runner.
The chat agent only passes the release asset name; it never serializes PNG
bytes or Base64 into a model message.
"""

from __future__ import annotations

import os
import re
import shutil
import stat
import struct
import sys
import tempfile
import zipfile
from pathlib import Path


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
MAX_MEMBER_BYTES = 32 * 1024 * 1024
MAX_ARCHIVE_BYTES = 512 * 1024 * 1024
CANONICAL_PREFIX = "docs/mockups/03-heroes/"
MEMBER_RE = re.compile(
    r"(?P<hero>lin_yue|soyeon_han)/"
    r"(?P<direction>[a-z_]+)/"
    r"(?P<state>[a-z0-9_]+)\.png"
)


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def normalize_member(name: str) -> str:
    normalized = name.replace("\\", "/")
    if "\x00" in normalized:
        fail("archive member contains a NUL byte")
    if normalized.startswith("/"):
        fail(f"absolute archive path is not allowed: {name!r}")

    parts = normalized.split("/")
    if ".." in parts:
        fail(f"path traversal is not allowed: {name!r}")
    parts = [part for part in parts if part not in ("", ".")]
    normalized = "/".join(parts)

    if normalized.startswith(CANONICAL_PREFIX):
        normalized = normalized[len(CANONICAL_PREFIX) :]
    return normalized


def validate_png(data: bytes, member: str) -> None:
    if len(data) < 29 or data[:8] != PNG_SIGNATURE:
        fail(f"{member}: not a PNG file")

    ihdr_length = struct.unpack(">I", data[8:12])[0]
    if data[12:16] != b"IHDR" or ihdr_length != 13:
        fail(f"{member}: missing or invalid PNG IHDR")

    width, height, bit_depth, color_type = struct.unpack(">IIBB", data[16:26])
    if (width, height) != (1024, 1024):
        fail(f"{member}: expected 1024x1024, got {width}x{height}")
    if bit_depth != 8 or color_type != 6:
        fail(
            f"{member}: expected 8-bit true RGBA PNG "
            f"(bit_depth=8, color_type=6), got "
            f"bit_depth={bit_depth}, color_type={color_type}"
        )


def expected_for(hero: str) -> set[str]:
    return {
        f"{hero}/{direction}/{state}.png"
        for direction in sorted(DIRECTIONS)
        for state in sorted(STATES)
    }


def main() -> int:
    if len(sys.argv) not in (2, 3):
        fail("usage: import_stage03_assets.py ARCHIVE.zip [TARGET_ROOT]")

    archive = Path(sys.argv[1])
    target_root = Path(sys.argv[2] if len(sys.argv) == 3 else "docs/mockups/03-heroes")
    if not archive.is_file():
        fail(f"archive does not exist: {archive}")
    if not target_root.is_dir():
        fail(f"target root does not exist: {target_root}")

    entries: dict[str, bytes] = {}
    total_uncompressed = 0

    try:
        with zipfile.ZipFile(archive) as package:
            for info in package.infolist():
                if info.is_dir():
                    continue

                file_mode = (info.external_attr >> 16) & 0o170000
                if file_mode == stat.S_IFLNK:
                    fail(f"symbolic links are not allowed: {info.filename!r}")
                if info.file_size <= 0 or info.file_size > MAX_MEMBER_BYTES:
                    fail(
                        f"{info.filename!r}: uncompressed member size is outside "
                        f"the allowed range"
                    )

                total_uncompressed += info.file_size
                if total_uncompressed > MAX_ARCHIVE_BYTES:
                    fail("archive exceeds the 512 MiB uncompressed safety limit")

                member = normalize_member(info.filename)
                match = MEMBER_RE.fullmatch(member)
                if not match:
                    fail(
                        f"unsupported archive member {info.filename!r}; "
                        "only hero/direction/state.png is accepted"
                    )
                if match.group("direction") not in DIRECTIONS:
                    fail(f"unsupported direction in {member}")
                if match.group("state") not in STATES:
                    fail(f"unsupported state in {member}")
                if member in entries:
                    fail(f"duplicate archive member after path normalization: {member}")

                data = package.read(info)
                if len(data) != info.file_size:
                    fail(f"short read while reading {member}")
                validate_png(data, member)
                entries[member] = data
    except zipfile.BadZipFile as exc:
        fail(f"invalid ZIP archive: {exc}")

    if not entries:
        fail("archive contains no PNG files")

    heroes_present = {member.split("/", 1)[0] for member in entries}
    if not heroes_present.issubset(HEROES):
        fail("archive contains an unknown hero directory")
    for hero in sorted(heroes_present):
        actual = {member for member in entries if member.startswith(f"{hero}/")}
        expected = expected_for(hero)
        if actual != expected:
            missing = sorted(expected - actual)
            extra = sorted(actual - expected)
            details = []
            if missing:
                details.append(f"missing={missing[:8]}{'...' if len(missing) > 8 else ''}")
            if extra:
                details.append(f"extra={extra[:8]}{'...' if len(extra) > 8 else ''}")
            fail(f"{hero} is incomplete ({'; '.join(details)})")

    target_root = target_root.resolve()
    destinations: dict[str, Path] = {}
    for member in sorted(entries):
        destination = (target_root / member).resolve()
        if target_root not in destination.parents:
            fail(f"resolved destination escaped target root: {member}")
        if destination.exists():
            fail(f"refusing to overwrite an existing file: {destination}")
        destinations[member] = destination

    temporary_root = Path(
        tempfile.mkdtemp(prefix=".stage03-import-", dir=str(target_root.parent))
    )
    try:
        for member, data in entries.items():
            staged = temporary_root / member
            staged.parent.mkdir(parents=True, exist_ok=True)
            staged.write_bytes(data)

        for member, destination in destinations.items():
            destination.parent.mkdir(parents=True, exist_ok=True)
            os.replace(temporary_root / member, destination)
    finally:
        shutil.rmtree(temporary_root, ignore_errors=True)

    display_root = Path(sys.argv[2] if len(sys.argv) == 3 else "docs/mockups/03-heroes")
    for member in sorted(entries):
        print(f"IMPORTED {(display_root / member).as_posix()}")
    print(
        "SUMMARY "
        f"heroes={','.join(sorted(heroes_present))} "
        f"files={len(entries)} "
        f"uncompressed_bytes={total_uncompressed}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
