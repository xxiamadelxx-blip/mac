"""Dependency-free verification of Blender's cloud-rendered technical PNG."""
import hashlib
import json
from pathlib import Path
import struct

out = Path(__file__).resolve().parent / "output"
png = out / "technical_smoke.png"
meta = json.loads((out / "technical_smoke.json").read_text(encoding="utf-8"))
assert png.exists() and png.stat().st_size > 1000, "PNG missing or too small"
header = png.read_bytes()[:26]
assert header[:8] == b"\x89PNG\r\n\x1a\n", "Not a PNG"
assert header[12:16] == b"IHDR", "No PNG IHDR"
width, height = struct.unpack(">II", header[16:24])
assert (width, height) == (256, 256), f"Unexpected image dimensions {(width, height)}"
assert header[25] == 6, "Expected RGBA PNG with alpha"
assert meta["png_sha256"] == hashlib.sha256(png.read_bytes()).hexdigest(), "SHA mismatch"
assert meta["production_approval"] is False, "Not production artwork"
print(f"CLOUD_BLENDER_PNG_VERIFIED: {width}x{height} RGBA bytes={png.stat().st_size}")
