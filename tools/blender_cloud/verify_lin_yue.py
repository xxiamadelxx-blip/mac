"""Inspect real Blender + glTF output and PNG alpha, do not auto-approve art."""
import json, hashlib, struct
from pathlib import Path

out=Path(__file__).resolve().parents[2]/"docs/mockups/03-heroes/3d-candidates/lin_yue"
m=json.loads((out/"lin_yue_manifest.json").read_text(encoding="utf-8"))
assert m["production_approval"] is False
assert m["status"]=="CANDIDATE"
assert m["mesh_objects"]>=30 and m["vertices"]>=2500,(m["mesh_objects"],m["vertices"])
blender=(out/m["editable_source"]).read_bytes()
assert blender.startswith(b"BLENDER"),"Not a Blender project"
glb=(out/m["portable_mesh"]).read_bytes()
assert glb[:4]==b"glTF" and struct.unpack_from("<I",glb,4)[0]==2,"Missing GLB"
assert struct.unpack_from("<I",glb,8)[0]==len(glb),"Incomplete GLB"
jlen=struct.unpack_from("<I",glb,12)[0]
assert glb[16:20]==b"JSON"
obj=json.loads(glb[20:20+jlen].decode("utf-8"))
assert len(obj.get("meshes",[]))>=30,("Not enough actual GLB geometry",len(obj.get("meshes",[])))
assert len(blender)>10000 and len(glb)>10000
for p in m["renders"]:
    b=(out/p).read_bytes()
    assert b[:8]==b"\x89PNG\r\n\x1a\n",p
    assert tuple(struct.unpack_from(">II",b,16))==(640,760),p
    assert b[25]==6,("RGB instead of RGBA",p)
    assert len(b)>20000,(p,len(b))
for file in m["files"]:
    data=(out/file["path"]).read_bytes()
    assert len(data)==file["size_bytes"]
    assert hashlib.sha256(data).hexdigest()==file["sha256"]
print("LIN_YUE_MODEL_VERIFIED",
      "meshes="+str(len(obj["meshes"])),
      "vertices="+str(m["vertices"]),
      "blend="+str(len(blender)),
      "glb="+str(len(glb)),
      "renders="+str(len(m["renders"])))
