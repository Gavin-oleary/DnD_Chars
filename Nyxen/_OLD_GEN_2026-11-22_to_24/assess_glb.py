"""Assess a generated GLB: eight-angle textured + clay renders, mesh statistics. Read-only on the source."""
import bpy,bmesh,sys,json,math,numpy as np
from pathlib import Path
from mathutils import Vector
a=sys.argv[sys.argv.index('--')+1:];glb=Path(a[0]);out=Path(a[1]);out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(glb))
obs=[o for o in bpy.data.objects if o.type=='MESH']
stats=[]
for o in obs:
    me=o.data;bm=bmesh.new();bm.from_mesh(me)
    nonman=sum(1 for e in bm.edges if not e.is_manifold);boundary=sum(1 for e in bm.edges if e.is_boundary)
    # connected components
    seen=set();comps=0;sizes=[]
    for v in bm.verts:
        if v.index in seen:continue
        comps+=1;stack=[v];n=0
        while stack:
            x=stack.pop()
            if x.index in seen:continue
            seen.add(x.index);n+=1;stack+=[e.other_vert(x) for e in x.link_edges]
        sizes.append(n)
    quads=sum(1 for f in me.polygons if len(f.vertices)==4);tris=sum(1 for f in me.polygons if len(f.vertices)==3)
    d=o.dimensions
    stats.append({'object':o.name,'vertices':len(me.vertices),'faces':len(me.polygons),'quads':quads,'tris':tris,'ngons':len(me.polygons)-quads-tris,'non_manifold_edges':nonman,'boundary_edges':boundary,'components':comps,'largest_components':sorted(sizes,reverse=True)[:6],
                  'uv_layers':[l.name for l in me.uv_layers],'materials':[m.name for m in me.materials if m],'images':sorted({n.image.name for m in me.materials if m and m.use_nodes for n in m.node_tree.nodes if n.type=='TEX_IMAGE' and n.image}),'dimensions_m':[round(d.x,4),round(d.y,4),round(d.z,4)],'shape_keys':[k.name for k in me.shape_keys.key_blocks] if me.shape_keys else [],'vertex_groups':len(o.vertex_groups),'armature':any(m.type=='ARMATURE' for m in o.modifiers)})
    bm.free()
    for p in me.polygons:p.use_smooth=True
sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.samples=32;sc.cycles.use_denoising=True
try:
    prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='CUDA';prefs.refresh_devices()
    for dv in prefs.devices:dv.use=dv.type=='CUDA'
    sc.cycles.device='GPU'
except Exception:pass
sc.render.resolution_x=600;sc.render.resolution_y=1150;sc.render.image_settings.file_format='PNG';sc.view_settings.view_transform='AgX'
w=bpy.data.worlds.new('w');w.use_nodes=True;w.node_tree.nodes['Background'].inputs[0].default_value=(.25,.25,.25,1);w.node_tree.nodes['Background'].inputs[1].default_value=.6;sc.world=w
pts=np.array([o.matrix_world@Vector(c) for o in obs for c in o.bound_box]);lo=pts.min(0);hi=pts.max(0);center=(lo+hi)/2;ext=float((hi-lo).max())
def light(name,off,e):
    d=bpy.data.lights.new(name,'AREA');d.energy=e;d.size=ext;o=bpy.data.objects.new(name,d);sc.collection.objects.link(o);o.location=Vector(center)+Vector(off)*ext;o.rotation_euler=(Vector(center)-o.location).to_track_quat('-Z','Y').to_euler()
light('key',(-1.5,-2,1.5),1500*ext*ext);light('fill',(2,-1,.8),700*ext*ext);light('rim',(0,2,1.5),900*ext*ext)
cam=bpy.data.objects.new('cam',bpy.data.cameras.new('cam'));sc.collection.objects.link(cam);cam.data.type='ORTHO';cam.data.ortho_scale=ext*1.1;sc.camera=cam
clay=bpy.data.materials.new('clay');clay.use_nodes=True;bs=clay.node_tree.nodes['Principled BSDF'];bs.inputs['Base Color'].default_value=(.42,.42,.42,1);bs.inputs['Roughness'].default_value=.7
angles={'FRONT':0,'FRONT-RIGHT':45,'RIGHT-PROFILE':90,'BACK-RIGHT':135,'BACK':180,'BACK-LEFT':225,'LEFT-PROFILE':270,'FRONT-LEFT':315}
rec={'stats':stats,'bounds_m':{'min':lo.tolist(),'max':hi.tolist()},'height_m':float(hi[2]-lo[2]),'renders':{}}
for mode in ['textured','clay']:
    sc.view_layers[0].material_override=clay if mode=='clay' else None
    for n,deg in angles.items():
        t=math.radians(deg);dvec=Vector((math.sin(t),-math.cos(t),0))   # 0 = front (-Y), 90 = viewer on +X side (right profile as the sheet labels it)
        cam.location=Vector(center)+dvec*ext*4;cam.rotation_euler=(Vector(center)-cam.location).to_track_quat('-Z','Y').to_euler()
        sc.render.filepath=str(out/f'{mode}_{n}.png');bpy.ops.render.render(write_still=True);rec['renders'][f'{mode}_{n}']=sc.render.filepath
(out/'assessment.json').write_text(json.dumps(rec,indent=1));print('ASSESS',json.dumps({'stats':stats,'height_m':rec['height_m']}))
