
import bpy
from bpy.props import StringProperty, PointerProperty, FloatProperty
import math
class materialCleanUpPanel(bpy.types.Panel):
    
    bl_label = "Material Clean-up"
    bl_idname = "MATCNUP_PT_PANEL"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Material"
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text = "SELECT a target mesh")
        row = layout.row()
        row.operator("mat.cleanup_operator")
        row = layout.row()
        row.operator("cam.setup_operator")
        
        scn = bpy.context.scene
        world = scn.world 
        row=layout.row()
        row.operator("hdri.setup_operator")
        row=layout.row()
        row.prop(world.my_hdri, "hdri")
        row=layout.row()
        row.prop(world.my_hdri, "degree")
        
        cam = scn.camera
        row = layout.row()
        row.prop(cam.my_transform, "distance")
        
class MAT_CLEARNUP(bpy.types.Operator):
    
    bl_label = "Material Cleanup"
    bl_idname = "mat.cleanup_operator"

    def execute(self,context):
        material= bpy.data.materials
        mat_list = [m for m in material]
    
        for mat in mat_list:
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            bsdf.inputs[5].default_value = 0
               
        return {"FINISHED"}
    
class CAM_SETUP(bpy.types.Operator):
    bl_label = "Camera Setup"
    bl_idname = "cam.setup_operator"
    
    def execute(self,context):
        
        loc = bpy.context.object.location
        camera = bpy.context.scene.camera
        rot = bpy.context.object.rotation_euler

        camera.location = (0.0, loc[1]-5, 0.0)
        camera.rotation_euler = (math.radians(90), 0, 0)
     
        return {"FINISHED"}
    
def updateCam(self,context):
    loc = bpy.context.object.location
    camera = bpy.context.scene.camera
    param = self.distance
    camera.location[1] = self.distance
    
class HDRI_MAP(bpy.types.Operator):
    bl_label = "HDRI Setup"
    bl_idname = "hdri.setup_operator"
    
    def execute(self, context):
        bpy.data.scenes["Scene"].render.engine = 'CYCLES'
        world = bpy.data.worlds['World']
        world.use_nodes = True
        
        env_light = world.node_tree.nodes['Background']
        env_light.inputs[1].default_value = 2.2
        env_tex = world.node_tree.nodes.new("ShaderNodeTexEnvironment")
        mapping = world.node_tree.nodes.new("ShaderNodeMapping")
        mapping.vector_type = "TEXTURE"
        mapping.inputs[2].default_value[2] = math.radians(45)
        world.node_tree.links.new(mapping.outputs[0], env_tex.inputs[0])
        texture_coord = world.node_tree.nodes.new("ShaderNodeTexCoord")
        world.node_tree.links.new(texture_coord.outputs[0], mapping.inputs[0])
        #TODO: set uv rotation.z to 45 degrees
        world.node_tree.links.new(env_tex.outputs[0], env_light.inputs[0])
       
        return {"FINISHED"}
def updatehdri(self,context):
    
    scn = bpy.context.scene
    world = scn.world
    node = world.node_tree.nodes
    coord = bpy.types.ShaderNodeTexEnvironment
    nodes = [s for s in node
            if isinstance (s, coord)]
    
    for n in nodes:
       n.image = bpy.data.images.load(self.hdri)
    

def setHdriRotation(self, context):
    scn = bpy.context.scene
    world = scn.world
    mapping_node = world.node_tree.nodes["Mapping"]
    
    mapping_node.inputs[2].default_value[2] = math.radians(self.degree)
            
class hdriSet(bpy.types.PropertyGroup):

    hdri: StringProperty(
            name="HDRI",
            subtype='FILE_PATH',
            update = updatehdri)
            
    degree: FloatProperty(
            name = "hdri rotation",
            subtype="NONE",
            min=0.0, max= 360.0,
            default=45.0,
            update=setHdriRotation)
class camSet(bpy.types.PropertyGroup):
    distance: FloatProperty(
            name = "Zoom In/Out",
            subtype="NONE",
            min=-200.0, max= 200.0,
            default=0.0,
            update=updateCam)
             

def register():
    bpy.utils.register_class(materialCleanUpPanel)
    bpy.utils.register_class(MAT_CLEARNUP)
    bpy.utils.register_class(CAM_SETUP)
    bpy.utils.register_class(HDRI_MAP)
    bpy.utils.register_class(hdriSet)
    bpy.utils.register_class(camSet)
    bpy.types.World.my_hdri = PointerProperty(type = hdriSet)
    bpy.types.Object.my_transform = PointerProperty(type = camSet)
def unregister():
    bpy.utils.unregister_class(materialCleanUpPanel)
    bpy.utils.unregister_class(MAT_CLEARNUP)
    bpy.utils.unregister_class(CAM_SETUP)
    bpy.utils.unregister_class(HDRI_MAP)
    bpy.utils.unregister_class(hdriSet)
    bpy.utils.unregister_class(camSet)
    del bpy.types.World.my_hdri
    del bpy.types.Object.my_transform

if __name__ == "__main__":
    register()