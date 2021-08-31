import bpy


material= bpy.data.materials


mat_list = [m for m in material]
print(mat_list)
    
for mat in mat_list:
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs[5].default_value = 0
    bsdf.inputs[4].default_value = 0
   
    