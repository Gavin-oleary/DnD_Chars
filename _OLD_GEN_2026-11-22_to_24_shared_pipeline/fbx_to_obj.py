import bpy,sys
src=sys.argv[sys.argv.index('--')+1];dst=sys.argv[sys.argv.index('--')+2]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=src)
for o in bpy.context.scene.objects:
    if o.type=='MESH':o.select_set(True)
bpy.ops.wm.obj_export(filepath=dst,export_selected_objects=True,export_uv=True,export_normals=False,export_materials=False,export_triangulated_mesh=False,apply_modifiers=True,forward_axis='NEGATIVE_Z',up_axis='Y')
print('OBJ',dst,sum(len(o.data.polygons) for o in bpy.context.scene.objects if o.type=='MESH'))
