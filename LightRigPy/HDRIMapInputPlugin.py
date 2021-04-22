bl_info ={
    "name": "HDRI Lighting Rig Plugin",
    "author" : "Kayla Man",
    "version" : (1,0),
    "blender" : (2,91,0),
    "location" : " ",
    "description" : "Customizing the path and intensity for users to import their HDRI maps",
    "warning": "", 
    "wiki_url": "",
    "category": "Light Rig"
}
import bpy
from bpy.props import StringProperty, PointerProperty, FloatProperty

class HdriLightPanel(bpy.types.Panel):
    
    bl_label = "HDRI Map Rig"
    bl_idname = "HDRI_PT_PANEL"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Light Rig"
    
    def draw(self, context):
        layout = self.layout
        scn = bpy.context.scene
        world = scn.world 
        row=layout.row()
        row.operator("env.light_operator")
        row=layout.row()
        row.operator("del.hdri_operator")
        row=layout.row()
        row.prop(world.my_hdri, "hdri")

class ENV_MAP(bpy.types.Operator):
    bl_label = "EnvLight"
    bl_idname = "env.light_operator"

    def execute(self,context):
        bpy.data.scenes["Scene"].render.engine = 'CYCLES'
        world = bpy.data.worlds['World']
        world.use_nodes = True
        
        env_light = world.node_tree.nodes['Background']
        env_tex = world.node_tree.nodes.new("ShaderNodeTexEnvironment")
        
        world.node_tree.links.new (env_tex.outputs[0], env_light.inputs[0])
       
        return {"FINISHED"}

class DELHDRI(bpy.types.Operator):
    bl_label = "Delete HDRI"
    bl_idname = "del.hdri_operator"

    def execute(self,context):
        wrd= bpy.data.worlds['World']
        node_del = wrd.node_tree.nodes["Environment Texture"]

        wrd.node_tree.nodes.remove( node_del )

        return{"FINISHED"}

def updatehdri(self,context):
    
    scn = bpy.context.scene
    world = scn.world
    node = world.node_tree.nodes
    coord = bpy.types.ShaderNodeTexEnvironment
    nodes = [s for s in node
            if isinstance (s, coord)]
    
    for i in range(len(nodes)):
        nodes[i].image = bpy.data.images.load(self.hdri)
    
    
        
class materialSet(bpy.types.PropertyGroup):

    hdri: StringProperty(
            name="HDRI",
            subtype='FILE_PATH',
            update = updatehdri)
             
def register():
    bpy.utils.register_class(HdriLightPanel)
    bpy.utils.register_class(ENV_MAP)
    bpy.utils.register_class(materialSet)
    bpy.utils.register_class(DELHDRI)
    bpy.types.World.my_hdri=PointerProperty(type=materialSet)

def unregister():
    bpy.utils.unregister_class(HdriLightPanel)
    bpy.utils.unregister_class(ENV_MAP)
    bpy.utils.unregister_class(DELHDRI)
    bpy.utils.unregister_class(materialSet)
    del bpy.types.World.my_hdri

if __name__ == "__main__":
    register()
