import bpy
import math

loc = bpy.context.object.location
camera = bpy.context.scene.camera
rot = bpy.context.object.rotation_euler

camera.location = (0.0, loc[1]-5, 0.0)
camera.rotation_euler = (math.radians(90), rot[1], rot[2])