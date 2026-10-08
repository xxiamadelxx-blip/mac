"""Technical headless Blender smoke test. No Moonveil production art is generated."""
import bpy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output"
OUT.mkdir(parents=True, exist_ok=True)
PNG = OUT / "technical_smoke.png"

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.cycles.samples = 8
# Ubuntu distribution build of Blender 4.0 lacks OpenImageDenoise at runtime.
# Disable render denoising, otherwise Cycles raises "Build without OpenImageDenoiser".
bpy.context.view_layer.cycles.use_denoising = False
scene.render.resolution_x = 256
scene.render.resolution_y = 256
scene.render.resolution_percentage = 100
scene.render.film_transparent = True
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGBA"
scene.render.filepath = str(PNG)

# Technical proof object only; it is not placed in a game asset directory.
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1.0)
obj = bpy.context.object
mat = bpy.data.materials.new(name="smoke-probe-surface")
mat.diffuse_color = (0.15, 0.7, 0.8, 1.0)
mat.use_nodes = True
node = mat.node_tree.nodes.get("Principled BSDF")
if node:
    node.inputs["Base Color"].default_value = (0.15, 0.7, 0.8, 1.0)
obj.data.materials.append(mat)

bpy.ops.object.camera_add(location=(3, -4, 2.5))
camera = bpy.context.object
rotation = (obj.location - camera.location).to_track_quat("-Z", "Y")
camera.rotation_euler = rotation.to_euler()
camera.data.type = "ORTHO"
camera.data.ortho_scale = 3.4
scene.camera = camera

bpy.ops.object.light_add(type="AREA", location=(0, -2, 4))
light = bpy.context.object
light.data.energy = 450.0
light.data.shape = "DISK"
light.data.size = 5.0

bpy.ops.render.render(write_still=True)
if not PNG.is_file():
    raise RuntimeError(f"Render output missing: {PNG}")

meta = {
    "kind": "TECHNICAL_SMOKE_ONLY_NOT_ART",
    "blender_version": bpy.app.version_string,
    "renderer": scene.render.engine,
    "dimensions": [256, 256],
    "png_file": PNG.name,
    "png_size_bytes": PNG.stat().st_size,
    "png_sha256": hashlib.sha256(PNG.read_bytes()).hexdigest(),
    "production_approval": False,
}
(OUT / "technical_smoke.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
print("CLOUD_BLENDER_SMOKE_OK: " + json.dumps(meta, ensure_ascii=False))
