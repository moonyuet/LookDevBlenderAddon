import bpy
import math

objects = bpy.context.active_object
empty = bpy.ops.object.empty_add(type= "PLAIN_AXES", align='WORLD', location = (0,0,0))
em = bpy.context.object
objects.parent = em
objects.matrix_parent_inverse = em.matrix_world.inverted()

em.rotation_euler[2] = math.radians(0)
em.keyframe_insert(data_path="rotation_euler", frame=1)
em.rotation_euler[2] = math.radians(360)
em.keyframe_insert(data_path="rotation_euler", frame=120)

for i in range (0, 1):
    frame = em.animation_data.action.fcurves[2].keyframe_points[i]
    frame.interpolation = 'LINEAR'
    
#TODO: allows users to customize the frame 
    