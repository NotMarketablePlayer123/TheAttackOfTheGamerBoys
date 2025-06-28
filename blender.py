import bpy
import math
from mathutils import Vector

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Body
bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=1, location=(0, 0, 1))
body = bpy.context.active_object
body.name = 'Body'
dec = body.modifiers.new(name='Decimate', type='DECIMATE')
dec.decimate_type = 'COLLAPSE'
dec.ratio = 0.4
bpy.ops.object.modifier_apply(modifier=dec.name)
body.scale = (1.2, 0.8, 1)

# Comb
bpy.ops.mesh.primitive_cone_add(vertices=5, radius1=0.2, depth=0.3, location=(0, 0, 1.9))
comb = bpy.context.active_object
comb.name = 'Comb'
comb.rotation_euler = (math.radians(90), 0, 0)

# Beak
bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.1, depth=0.3, location=(0.4, 0, 1.2))
beak = bpy.context.active_object
beak.name = 'Beak'
beak.rotation_euler = (0, math.radians(90), 0)

# Wattle
bpy.ops.mesh.primitive_cube_add(size=0.2, location=(0.2, -0.1, 1.0))
wattle = bpy.context.active_object
wattle.name = 'Wattle'
wattle.scale = (0.5, 0.2, 1)

# Wings
for side in [1, -1]:
    bpy.ops.mesh.primitive_plane_add(size=0.5, location=(0, side * 0.8, 1))
    wing = bpy.context.active_object
    wing.name = f'Wing_{side}'
    wing.rotation_euler = (0, 0, math.radians(45 * side))

# Eyes
for idx, x in enumerate([-0.2, 0.2]):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=8, ring_count=4, radius=0.1, location=(x, 0.2, 1.4))
    eye = bpy.context.active_object
    eye.name = f'Eye_{idx}'

# Emblem background
bpy.ops.mesh.primitive_plane_add(size=0.4, location=(0, 0.8, 1))
emblem = bpy.context.active_object
emblem.name = 'Emblem'

# Flat shading for all meshes
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.shade_flat()

# Save the Blender file
bpy.ops.wm.save_as_mainfile(filepath="/mnt/data/super_hyper_chicken.blend")
