"""Moonveil Lin Yue: editable non-production 3D character concept.
Native Blender geometry and materials. No existing 2D asset is modified.
"""
import bpy, math, json, hashlib, struct
from pathlib import Path
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/"docs/mockups/03-heroes/3d-candidates/lin_yue"
OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)

groups={}
for n in ["Body","Clothing","Hair","Jewelry","Talismans","MoonFan","Studio"]:
    col=bpy.data.collections.new(n)
    bpy.context.scene.collection.children.link(col)
    groups[n]=col
group="Body"

def move(o,name):
    o.name=name
    for c in tuple(o.users_collection): c.objects.unlink(o)
    groups[group].objects.link(o)
    return o

def mat(name,col,rough=.72,metal=0):
    m=bpy.data.materials.new(name)
    m.diffuse_color=(*col,1)
    m.use_nodes=True
    b=m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value=(*col,1)
    b.inputs["Roughness"].default_value=rough
    b.inputs["Metallic"].default_value=metal
    return m
skin=mat("Warm porcelain",(.78,.60,.51))
blush=mat("Mutest rose",(.61,.31,.34))
hair=mat("Ink teal",(.029,.070,.077),.4)
hair_high=mat("Hair glint",(.06,.14,.14),.5)
black=mat("Soft ink",(.022,.036,.037))
iris=mat("Jade pupils",(.085,.35,.31),.28)
white=mat("Ivory eyes",(.94,.86,.74))
jade=mat("Sea glass green",(.43,.66,.58))
mist=mat("Pale mint silk",(.66,.78,.68))
ivory=mat("Moon ivory",(.85,.81,.72))
sash=mat("Deep teal",(.12,.34,.32))
silver=mat("Brushed moon silver",(.67,.75,.75),.28,.72)
gold=mat("Antique pearl brass",(.69,.61,.45),.29,.58)
pearl=mat("Jade enamel",(.47,.84,.73),.17,.3)
sole=mat("Charcoal boots",(.065,.09,.10))
def apply(o,m):
    o.data.materials.append(m)
    if o.type=="MESH":
        for poly in o.data.polygons: poly.use_smooth=True
    return o

def uv(name,xyz,scale,m):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=20,location=xyz)
    o=move(bpy.context.object,name);o.scale=scale
    return apply(o,m)

def rod(name,a,b,r,m):
    a,b=Vector(a),Vector(b)
    bpy.ops.mesh.primitive_cylinder_add(vertices=12,radius=r,depth=(b-a).length,location=(a+b)/2)
    o=move(bpy.context.object,name)
    o.rotation_euler=(b-a).to_track_quat("Z","Y").to_euler()
    return apply(o,m)

def objmesh(name,verts,faces,m):
    mesh=bpy.data.meshes.new(name+"_mesh")
    mesh.from_pydata(verts,[],faces);mesh.update()
    o=bpy.data.objects.new(name,mesh);groups[group].objects.link(o)
    return apply(o,m)

def stroke(name,pts,m,r=.012,rad=None,closed=False):
    c=bpy.data.curves.new(name,"CURVE");c.dimensions="3D";c.resolution_u=16;c.bevel_depth=r;c.bevel_resolution=3
    s=c.splines.new("POLY");s.points.add(len(pts)-1)
    for i,p in enumerate(pts):
        s.points[i].co=(*p,1)
        if rad: s.points[i].radius=rad[i]
    s.use_cyclic_u=closed
    o=bpy.data.objects.new(name,c);groups[group].objects.link(o);c.materials.append(m)
    return o

def ellipsoid_loft(name,levels,m,segments=48):
    vs=[]
    for z,rx,ry in levels:
        for i in range(segments):
            ang=2*math.pi*i/segments
            vs.append((rx*math.sin(ang),-ry*math.cos(ang),z))
    fs=[]
    for j in range(len(levels)-1):
        for i in range(segments):
            nxt=(i+1)%segments
            fs.append((j*segments+i,j*segments+nxt,(j+1)*segments+nxt,(j+1)*segments+i))
    fs.extend([tuple(reversed(range(segments))),tuple((len(levels)-1)*segments+i for i in range(segments))])
    return objmesh(name,vs,fs,m)

def frontal_panel(name,levels,widths,m,extra=.019):
    n=18;v=[]
    for (z,rx,ry),width in zip(levels,widths):
        for i in range(n+1):
            a=-width+2*width*i/n
            v.append(((rx+extra)*math.sin(a),-(ry+extra)*math.cos(a),z))
    f=[]
    for j in range(len(levels)-1):
        for i in range(n):
            f.append((j*(n+1)+i,j*(n+1)+i+1,(j+1)*(n+1)+i+1,(j+1)*(n+1)+i))
    o=objmesh(name,v,f,m);o.modifiers.new("Real silk panel thickness","SOLIDIFY").thickness=.008
    return o

# Footwear
uv("Left rounded boot",(-.18,-.05,.145),(.14,.25,.13),sole)
uv("Right rounded boot",(.18,-.05,.145),(.14,.25,.13),sole)
group="Clothing"
skirt=[
 (.17,.74,.52),(.31,.77,.54),(.65,.67,.47),
 (1.02,.52,.39),(1.34,.39,.31),(1.69,.28,.24),
 (1.92,.245,.22),(2.08,.26,.22)]
ellipsoid_loft("Floor-length pleated jade hanfu skirt",skirt,jade)
frontal_panel("Moon ivory center fold",skirt,[.29,.30,.34,.36,.35,.30,.25,.24],ivory)
frontal_panel("Mint central overfold",skirt,[.1,.1,.11,.14,.15,.15,.10,.09],mist,.04)
for a in [-.42,.42,-.76,.76]:
    pts=[(rx*math.sin(a)*1.024,-ry*math.cos(a)*1.024,z) for z,rx,ry in skirt[:7]]
    stroke("Jade embroidered pleat",pts,sash,.006)
hem=[(.77*math.sin(i*math.tau/90),-.54*math.cos(i*math.tau/90),.29) for i in range(90)]
stroke("Antique gold silk hem",hem,gold,.008,closed=True)
ellipsoid_loft("Cross-wrapped ivory upper robe",[
 (1.83,.235,.205),(2.00,.245,.21),(2.20,.283,.218),
 (2.41,.365,.244),(2.55,.30,.215),(2.63,.16,.15)],ivory)
objmesh("Right crossed jade collar",[(0,-.23,2.64),(.16,-.251,2.54),(.28,-.23,2.17),(.10,-.23,2.24)],[(0,1,2,3)],jade)
objmesh("Left crossed teal collar",[(0,-.24,2.64),(-.16,-.251,2.54),(-.28,-.23,2.17),(-.10,-.24,2.24)],[(0,1,2,3)],sash)
stroke("Collar right piping",[(0,-.25,2.62),(.15,-.263,2.51),(.27,-.24,2.18)],silver,.008)
stroke("Collar left piping",[(0,-.25,2.62),(-.15,-.263,2.51),(-.27,-.24,2.18)],silver,.008)
ellipsoid_loft("Wide teal waist sash",[(1.84,.28,.246),(1.9,.295,.247),(2.03,.285,.232),(2.08,.272,.229)],sash)
uv("Silver moon waist medallion",(0,-.279,1.967),(.105,.026,.085),silver)
uv("Jade inset jewel",(0,-.309,1.967),(.069,.019,.059),pearl)
# Real 3D bell-shaped sleeves along a tapered bone-axis. 
def sleeve(sign,label):
    A=Vector((sign*.34,-.03,2.46));B=Vector((sign*.90,-.18,1.85))
    direction=(B-A).normalized()
    across=direction.cross(Vector((0,1,0))).normalized()
    normal=direction.cross(across).normalized()
    stages=[(0,.142),(.22,.175),(.43,.22),(.68,.29),(.85,.32),(1,.31)]
    n=32;v=[];f=[]
    for t,r in stages:
        p=A.lerp(B,t)
        for i in range(n):
            a=math.tau*i/n
            q=p+across*r*math.cos(a)+normal*r*.72*math.sin(a)
            v.append(tuple(q))
    for j in range(len(stages)-1):
        for i in range(n):
            f.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
    objmesh(label+" wide layered sleeve",v,f,mist)
    P=A.lerp(B,.88)
    ring=[tuple(P+across*.315*math.cos(i*math.tau/36)+normal*.232*math.sin(i*math.tau/36)) for i in range(36)]
    stroke(label+" silver embroidered cuff",ring,silver,.011,closed=True)
    uv(label+" hand",(sign*.91,-.21,1.76),(.098,.092,.166),skin)
    stroke(label+" silk dangling thread",[(sign*.99,-.20,1.74),(sign*1.06,-.17,1.47),(sign*1.11,-.15,1.35)],gold,.012,[1,.8,.3])
for sign,name in [(-1,"Left"),(1,"Right")]:sleeve(sign,name)

group="Body"
rod("Neck",(0,0,2.58),(0,0,2.83),.105,skin)
uv("Head",(0,-.04,3.165),(.33,.267,.433),skin)
for sign,name in [(-1,"Left"),(1,"Right")]:
    uv(name+" ear",(sign*.328,-.015,3.152),(.055,.035,.09),skin)
    uv(name+" almond ivory sclera",(sign*.128,-.294,3.215),(.097,.027,.064),white)
    uv(name+" dimensional jade iris",(sign*.128,-.322,3.212),(.049,.019,.059),iris)
    uv(name+" dark pupil",(sign*.128,-.337,3.213),(.022,.009,.041),black)
    uv(name+" eye white shine",(sign*.14,-.350,3.24),(.009,.007,.013),ivory)
    stroke(name+" upper dark eyelash",[(sign*.034,-.295,3.255),(sign*.126,-.327,3.270),(sign*.229,-.29,3.249)],black,.013)
    stroke(name+" fine eyebrow",[(sign*.069,-.273,3.343),(sign*.143,-.286,3.355),(sign*.224,-.266,3.335)],hair,.010)
    uv(name+" subtle cheek",(sign*.18,-.270,3.05),(.063,.009,.029),blush)
uv("Small delicate nose",(0,-.309,3.104),(.026,.025,.045),skin)
stroke("Soft closed smile",[(-.05,-.287,3.00),(0,-.315,2.994),(.05,-.287,3.00)],blush,.008)

group="Hair"
uv("Crown volume",(0,.052,3.4),(.35,.30,.286),hair)
uv("Flowing curtain behind shoulders",(0,.16,2.75),(.36,.174,.90),hair)
uv("Midnight end of hair",(0,.20,2.05),(.22,.14,.31),hair)
for i in range(13):
    x=(i-6)*.051
    stroke("Editable long hair lock "+str(i),[
        (x*.75,.08,3.54),(x,.22,3.11),(x*1.12,.25,2.7),
        (x*1.06,.22,2.22),(x+(0.02 if i%2 else -.02),.22,1.9+(i%3)*.065)],
        hair_high if i%4==0 else hair,.021,[.7,1,1,.8,.07])
for s,tag in [(-1,"Left"),(1,"Right")]:
    stroke(tag+" long face framing lock",[
        (s*.30,-.08,3.48),(s*.347,-.17,3.19),(s*.39,-.16,2.92),
        (s*.46,-.13,2.49),(s*.47,-.11,2.2)],hair,.052,[.64,1,1,.68,.12])
for i in range(9):
    x=-.29+i*.072
    stroke("Individual swept bangs "+str(i),[
        (x,.005,3.58),(x,-.20,3.48),(x+(.03 if i%2==0 else -.02),-.269,3.346+.025*(i%3))],
        hair,.039,[.85,1,.05])

group="Jewelry"
for s,tag in [(-1,"Left"),(1,"Right")]:
    uv(tag+" earring silver setting",(s*.35,-.03,3.115),(.03,.026,.046),silver)
    stroke(tag+" pendant chain",[(s*.357,-.03,3.10),(s*.365,-.02,2.95)],silver,.009)
    uv(tag+" hanging jade bead",(s*.365,-.02,2.916),(.041,.04,.071),pearl)
stroke("Crescent moon upper hairpin",[
 (-.11,-.254,3.64),(-.18,-.257,3.72),(-.18,-.26,3.805),
 (-.11,-.262,3.883),(-.03,-.261,3.9),(-.104,-.273,3.851),
 (-.119,-.273,3.782),(-.092,-.271,3.721)],silver,.029,
 [.4,1,1,1,.13,.7,.9,.2])
uv("Crescent inset jade moonstone",(-.095,-.277,3.665),(.048,.025,.052),pearl)
for i in range(3):
    x=-.21+i*.075
    stroke("Hairpin ornamental chain "+str(i),[(x,-.21,3.65),(x-.01,-.21,3.52-i*.025)],silver,.006)
    uv("Jade comb bead "+str(i),(x-.01,-.215,3.52-i*.025),(.021,.024,.037),pearl)

group="Talismans"
for i,(x,y,z) in enumerate([(-.17,-.33,1.66),(.16,-.34,1.69),(.31,-.27,1.57)]):
    stroke("Woven belt cord "+str(i),[(x,-.25,1.91),(x,y,z+.16)],gold,.009)
    w=.095;h=.24
    objmesh("Talisman scroll "+str(i),
            [(x-w,y,z+h/2),(x+w,y,z+h/2),(x+w,y,z-h/2),(x-w,y,z-h/2)],
            [(0,1,2,3)],ivory)
    stroke("Moon seal calligraphy "+str(i),[
        (x-w*.45,y-.008,z+h*.23),(x+w*.25,y-.008,z+h*.17),
        (x+w*.05,y-.008,z-h*.02),(x-w*.25,y-.008,z-h*.16),
        (x+w*.28,y-.008,z-h*.28)],sash,.013)

group="MoonFan"
cx,cy,cz=1.12,-.27,1.95;R=.56
fan=[(cx,cy,cz)]
for i in range(25):
    a=math.radians(18+144*i/24)
    fan.append((cx+R*math.cos(a),cy,cz+R*math.sin(a)))
objmesh("Ivory silk folding moon fan",fan,[(0,i,i+1) for i in range(1,25)],mist)
stroke("Fan silver edge",fan[1:],silver,.011)
for i in range(13):
    a=math.radians(18+144*i/12)
    stroke("Foldable fan rib "+str(i),[(cx,cy-.015,cz),
     (cx+R*math.cos(a),cy-.017,cz+R*math.sin(a))],gold,.007)
rod("Fan hardwood stem",(.82,-.30,1.77),(cx,cy-.023,cz),.024,sash)
uv("Fan pivot pearl",(cx,cy-.03,cz),(.037,.016,.04),silver)
stroke("Fan painted lunar crest",[(cx-.07,cy-.03,cz+.30),(cx,cy-.03,cz+.35),
      (cx+.03,cy-.03,cz+.29),(cx-.02,cy-.03,cz+.27)],silver,.010)

# Studio, saved inside editable blend but excluded from game GLB
group="Studio"
scene=bpy.context.scene
world=scene.world;world.use_nodes=True
world.node_tree.nodes["Background"].inputs["Color"].default_value=(.11,.16,.16,1)
world.node_tree.nodes["Background"].inputs["Strength"].default_value=.65
for name,loc,power,size in [
 ("Key softbox",(-4,-5,6),600,4),
 ("Cool fill",(4,-1,4.6),500,4),
 ("Silver rim",(1,4,5.1),700,3)]:
    bpy.ops.object.light_add(type="AREA",location=loc)
    o=move(bpy.context.object,name);o.data.energy=power;o.data.shape="DISK";o.data.size=size
bpy.ops.object.camera_add(location=(0,-8,4))
camera=move(bpy.context.object,"Orthographic hero camera")
scene.camera=camera
camera.data.type="ORTHO";camera.data.ortho_scale=4.6
def aim(cam,target):
    cam.rotation_euler=(Vector(target)-cam.location).to_track_quat("-Z","Y").to_euler()
aim(camera,(0,0,1.96))
scene.render.engine="CYCLES";scene.cycles.device="CPU";scene.cycles.samples=12
bpy.context.view_layer.cycles.use_denoising=False
scene.render.resolution_x=640;scene.render.resolution_y=760;scene.render.resolution_percentage=100
scene.render.film_transparent=True
scene.render.image_settings.file_format="PNG";scene.render.image_settings.color_mode="RGBA"
scene.view_settings.view_transform="Standard"
scene.render.image_settings.compression=55

# Native authoring source with separately editable ornaments, fabrics, hair.
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/"lin_yue_editable.blend"))
# GLB export of native meshes + converted DUPLICATES of curve shapes.
curves=[o for o in bpy.data.objects if o.type=="CURVE"]
duplicates=[]
for original in curves:
    duplicate=original.copy();duplicate.data=original.data.copy()
    groups["MoonFan"].objects.link(duplicate)
    bpy.ops.object.select_all(action="DESELECT")
    duplicate.select_set(True);bpy.context.view_layer.objects.active=duplicate
    bpy.ops.object.convert(target="MESH")
    duplicates.append(bpy.context.view_layer.objects.active)
for original in curves:
    original.hide_set(True);original.hide_render=True
bpy.ops.object.select_all(action="DESELECT")
for o in bpy.data.objects:
    if o.type=="MESH" and o.users_collection[0].name!="Studio":o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(OUT/"lin_yue_portable.glb"),
   export_format="GLB",use_selection=True,export_cameras=False,export_lights=False)
for original in curves:
    original.hide_set(False);original.hide_render=False
for du in duplicates:bpy.data.objects.remove(du,do_unlink=True)

for name,pos in [
 ("front",(0,-8,4.0)),("three_quarter",(5,-7,4.4)),
 ("side",(8,0,4.0)),("back",(0,8,4.0))]:
    camera.location=pos;aim(camera,(0,0,1.96))
    scene.render.filepath=str(OUT/("lin_yue_"+name+".png"))
    bpy.ops.render.render(write_still=True)
    print("LIN_YUE_RENDER_OK "+name,flush=True)

meshes=[o for o in bpy.data.objects if o.type=="MESH"]
files=[]
for f in sorted(OUT.iterdir()):
    if f.is_file():
        data=f.read_bytes()
        files.append({"path":f.name,"size_bytes":len(data),"sha256":hashlib.sha256(data).hexdigest()})
data={
 "candidate_id":"vl-20261009-lin-yue-3d-proposal-v01",
 "asset_id":"hero_lin_yue_3d_concept","family_id":"moonveil-jade-witch-3d",
 "route":"SPRITE","status":"CANDIDATE",
 "technical_status":"AWAITING_ACTIONS_VERIFICATION",
 "artistic_status":"PENDING_USER_REVIEW","production_approval":False,
 "identity_fidelity":"UNVERIFIED: missing full-body 2D source in live GitHub main",
 "source":"GAME_MANIFEST.md section 5 (pale jade dress, sleeves, talismans, silver moon jewelry, lunar fan)",
 "editable_source":"lin_yue_editable.blend","portable_mesh":"lin_yue_portable.glb",
 "blender_version":bpy.app.version_string,
 "mesh_objects":len(meshes),"vertices":sum(len(o.data.vertices) for o in meshes),
 "renders":["lin_yue_front.png","lin_yue_three_quarter.png","lin_yue_side.png","lin_yue_back.png"],
 "render_dimensions":[640,760],"files":files
}
(OUT/"lin_yue_manifest.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print("LIN_YUE_MODEL_CREATED "+json.dumps({"meshes":data["mesh_objects"],"vertices":data["vertices"],"blender":data["blender_version"],"files":len(files)},ensure_ascii=False),flush=True)
