import bpy, bmesh, sys, os, json, math
argv = sys.argv[sys.argv.index('--')+1:]
src, outdir = argv[0], argv[1]
os.makedirs(outdir, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
if src.lower().endswith('.fbx'):
    bpy.ops.import_scene.fbx(filepath=src)
else:
    bpy.ops.wm.obj_import(filepath=src)
meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
stats=[]
for o in meshes:
    bm=bmesh.new(); bm.from_mesh(o.data)
    quads=sum(1 for f in bm.faces if len(f.verts)==4)
    tris=sum(1 for f in bm.faces if len(f.verts)==3)
    ngons=len(bm.faces)-quads-tris
    nonman=sum(1 for e in bm.edges if not e.is_manifold)
    bound=sum(1 for e in bm.edges if e.is_boundary)
    # components
    seen=set(); comps=0
    for v in bm.verts:
        if v.index in seen: continue
        comps+=1; stack=[v]
        while stack:
            x=stack.pop()
            if x.index in seen: continue
            seen.add(x.index)
            for e in x.link_edges:
                y=e.other_vert(x)
                if y.index not in seen: stack.append(y)
    poles=sum(1 for v in bm.verts if len(v.link_edges) not in (4,) and not v.is_boundary)
    dims=[round(d,4) for d in o.dimensions]
    stats.append(dict(name=o.name,verts=len(bm.verts),faces=len(bm.faces),quads=quads,tris=tris,ngons=ngons,
        non_manifold_edges=nonman,boundary_edges=bound,components=comps,non4_valence_verts=poles,
        uv_layers=[u.name for u in o.data.uv_layers],dimensions=dims,materials=[m.name for m in o.data.materials if m]))
    bm.free()
json.dump(stats,open(os.path.join(outdir,'stats.json'),'w'),indent=1)
print(json.dumps(stats,indent=1))
# renders: textured + wire-clay from 4 angles
sc=bpy.context.scene
sc.render.engine='CYCLES'; sc.cycles.samples=32; sc.cycles.device='GPU'
sc.render.resolution_x=600; sc.render.resolution_y=1000
prefs=bpy.context.preferences.addons['cycles'].preferences
prefs.compute_device_type='OPTIX' if hasattr(prefs,'compute_device_type') else None
for d in prefs.devices: d.use=True
sc.render.film_transparent=False
w=bpy.data.worlds.new('W'); sc.world=w; w.use_nodes=True
w.node_tree.nodes['Background'].inputs[0].default_value=(0.35,0.35,0.35,1); w.node_tree.nodes['Background'].inputs[1].default_value=1.0
import mathutils
mins=mathutils.Vector((1e9,)*3); maxs=mathutils.Vector((-1e9,)*3)
for o in meshes:
    for c in o.bound_box:
        p=o.matrix_world@mathutils.Vector(c)
        mins=mathutils.Vector(map(min,mins,p)); maxs=mathutils.Vector(map(max,maxs,p))
center=(mins+maxs)/2; h=(maxs-mins).z
cam=bpy.data.cameras.new('C'); cam.type='ORTHO'; cam.ortho_scale=h*1.1
co=bpy.data.objects.new('Cam',cam); sc.collection.objects.link(co); sc.camera=co
sun=bpy.data.lights.new('S','SUN'); sun.energy=3; so=bpy.data.objects.new('Sun',sun); sc.collection.objects.link(so)
so.rotation_euler=(math.radians(50),0,math.radians(30))
clay=bpy.data.materials.new('clay'); clay.use_nodes=True
clay.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(0.8,0.8,0.8,1)
vl=sc.view_layers[0]
for label,ang in [('FRONT',0),('RIGHT',90),('BACK',180),('FRONT-LEFT',315)]:
    t=math.radians(ang)
    dvec=mathutils.Vector((math.sin(t),-math.cos(t),0))
    co.location=center+dvec*10
    co.rotation_euler=(math.radians(90),0,t)
    vl.material_override=None
    sc.render.filepath=os.path.join(outdir,f'textured_{label}.png'); bpy.ops.render.render(write_still=True)
    vl.material_override=clay
    sc.render.filepath=os.path.join(outdir,f'clay_{label}.png'); bpy.ops.render.render(write_still=True)
# wireframe close-up of head, front, workbench
sc.render.engine='BLENDER_WORKBENCH'
sc.display.shading.light='FLAT'; sc.display.shading.color_type='SINGLE'; sc.display.shading.show_object_outline=False
sc.display.shading.show_wire=False
for o in meshes:
    o.show_wire=True; o.show_all_edges=True
sc.display.shading.type='SOLID' if hasattr(sc.display.shading,'type') else None
vl.material_override=None
sc.render.resolution_x=1000; sc.render.resolution_y=1000
cam.ortho_scale=h*0.22
head=mathutils.Vector((center.x,center.y,maxs.z-h*0.09))
for label,ang in [('FRONT',0),('RIGHT',90)]:
    t=math.radians(ang); dvec=mathutils.Vector((math.sin(t),-math.cos(t),0))
    co.location=head+dvec*10; co.rotation_euler=(math.radians(90),0,t)
    sc.render.filepath=os.path.join(outdir,f'wire_head_{label}.png')
    try:
        bpy.context.scene.display.shading.show_wire = True
    except Exception as e: print('wire', e)
    bpy.ops.render.render(write_still=True)
print('DONE')
