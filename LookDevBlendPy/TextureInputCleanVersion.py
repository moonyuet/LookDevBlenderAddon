bl_info ={
    "name": "Material Creation",
    "author" : "Kayla Man",
    "version" : (3,0),
    "blender" : (2,91,0),
    "location" : " ",
    "description" : "importing textures into PBR Shader",
    "warning": "", 
    "wiki_url": "",
    "category": "Material Creation"
}
import bpy
from bpy.props import StringProperty, PointerProperty, FloatProperty

class MaterialTexturePanel(bpy.types.Panel):
    
    bl_label = "PBR Shader Add-on"
    bl_idname = "MATERIAL_PT_PANEL"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Material Creation"
    
    def draw(self, context):
        layout = self.layout
        ob = bpy.context.active_object
        ma =ob.active_material
        row=layout.row()
        row.operator("shader.pbr_operator")
        row=layout.row()
        layout.prop(ma, "name")
        row=layout.row()
        row.prop(ma.slot_setting, "diffuse")
        row=layout.row()
        row.prop(ma.slot_setting, "size")

class PBR_SHADER(bpy.types.Operator):
    
    bl_label = "PBR"
    bl_idname = "shader.pbr_operator"

    def execute(self,context):    
        activeObject = bpy.context.active_object
        mat_pbr = bpy.data.materials.new(name="PBR Shader")
        mat_pbr.use_nodes = True
        activeObject.data.materials.append(mat_pbr)              
        bsdf = mat_pbr.node_tree.nodes.get("Principled BSDF")

        map_node = mat_pbr.node_tree.nodes.new("ShaderNodeMapping")
        map_node.vector_type = 'TEXTURE'
        text_coord = mat_pbr.node_tree.nodes.new("ShaderNodeTexCoord")
        texture_list = []
        max_count = 5
        
        for i in range(0, max_count):
            texture_map = mat_pbr.node_tree.nodes.new("ShaderNodeTexImage")
            texture_list.append(texture_map)
            mat_pbr.node_tree.links.new(text_coord.outputs[2], map_node.inputs[0])
            mat_pbr.node_tree.links.new(map_node.outputs[0], texture_list[i].inputs[0])
            
            mat_pbr.node_tree.links.new(texture_list[0].outputs[0], bsdf.inputs[0])          
                #normal map
        nrm_node = mat_pbr.node_tree.nodes.new("ShaderNodeNormalMap")

        mat_pbr.node_tree.links.new(texture_list[1].outputs[0],nrm_node.inputs[1])
        mat_pbr.node_tree.links.new (nrm_node.outputs[0], bsdf.inputs[19])
                #roughness map
        mat_pbr.node_tree.links.new(texture_list[2].outputs[0], bsdf.inputs[7])      
                #metallic map
        mat_pbr.node_tree.links.new(texture_list[3].outputs[0], bsdf.inputs[4])
                #disaplacement map
        mat_output = mat_pbr.node_tree.nodes.get("Material Output")
        disp_node = mat_pbr.node_tree.nodes.new("ShaderNodeDisplacement")
        mat_pbr.node_tree.links.new(texture_list[4].outputs[0], disp_node.inputs[0])
        mat_pbr.node_tree.links.new(disp_node.outputs[0],mat_output.inputs[2])
        return {'FINISHED'}   

def updateMaterial(self, context):
    
    mat = self.id_data
    node = mat.node_tree.nodes
    img = bpy.types.ShaderNodeTexImage
    nodes = [k for k in node
            if isinstance(k,img)]
    source_path = self.diffuse
    texture_list = []
    texture_list.append(source_path)
    
    path_split = source_path.split("_")
    extension_split = path_split[1].split(".")
    texture_format_list = ["nrm", "rough", "mtl", "disp"]
    for t in texture_format_list:
        texture_path = source_path.replace(extension_split[0], t)
        texture_list.append(texture_path)
    for i in range(0, len(texture_list)):
        nodes[i].image = bpy.data.images.load(texture_list[i])     
    return nodes

def updateRepeat(self, context):
        mat = self.id_data
        node = mat.node_tree.nodes
        coord = bpy.types.ShaderNodeMapping
        nodes = [s for s in node
                if isinstance (s, coord)]
        for s in nodes:
                s.inputs[3].default_value[0] = self.size
                s.inputs[3].default_value[1] = self.size
        
class materialSet(bpy.types.PropertyGroup):

    diffuse: StringProperty(
            name="Diffuse",
            subtype='FILE_PATH',
            update = updateMaterial) 
    size: FloatProperty(
            name="Repeat",
            subtype='NONE',
            default=1.0,
            min=0, max=10,
            update = updateRepeat) 
   
def register():
    bpy.utils.register_class(MaterialTexturePanel)
    bpy.utils.register_class(PBR_SHADER)
    bpy.utils.register_class(materialSet)
    bpy.types.Material.slot_setting=PointerProperty(type=materialSet)
    
def unregister():
    bpy.utils.unregister_class(MaterialTexturePanel)
    bpy.utils.unregister_class(PBR_SHADER)
    bpy.utils.unregister_class(materialSet)
    del bpy.types.Material.slot_setting

if __name__ == "__main__":
    register()




