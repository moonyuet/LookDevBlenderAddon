import bpy
scn = bpy.context.scene
render = scn.render
render.engine = "CYCLES"
#allow users to set the reslution
render.resolution_x = 2048 
render.resolution_y = 2048
render.film_transparent = True
cycles = scn.cycles
cycles.device = "GPU"
cycles.progressive = "BRANCHED_PATH"