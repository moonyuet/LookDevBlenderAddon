import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, PointerProperty, FloatProperty
import math
import webbrowser
class BlendertoVsiticherPanel(bpy.types.Panel):
    
    bl_label = "Blender Plugin For Users from VStitcher"
    bl_idname = "MATCNUP_PT_PANEL"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Material"
    
    def draw(self, context):
        layout = self.layout
    
        row = layout.row()
        row.operator("delete_template_scene.operator")
        row = layout.row()
        row.operator("import_mesh.data_operator")
        row.operator("help.web_operator")
       
        scn = bpy.context.scene
        world = scn.world
        row = layout.row()
        row.label(text="Set / Delete HDRI") 
        row=layout.row()
        row.operator("hdri.setup_operator")
        row.operator("del.hdri_operator")
        row=layout.row()
        row.prop(world.my_hdri, "hdri")
        row.prop(world.my_hdri, "degree")   
        
        row = layout.row()
        row.label(text = "Set Camera")
        row = layout.row()
        row.operator("cam.setup_operator")
        
        cam = scn.camera
        row = layout.row()
        row.prop(cam.my_transform, "distance")
        row.prop(cam.my_transform, "elevation")
        
        row = layout.row()
        row.label(text = "Set Turntable")
        row = layout.row()
        row.operator("turntable.setup_operator")
        row.operator("delete.turntable_operator")

        obj = bpy.context.active_object
        ma = obj.active_material
        
        row = layout.row()
        row.label(text = "PBR Material Creation")
        row = layout.row()
        row.operator("shader.pbr_operator")
        row.operator("mat.cleanup_operator")
    
        row = layout.row()
        row.prop(ma.slot_setting, "diffuse")
        row.prop(ma.slot_setting, "size")
        
class DeleteTemplateScene(bpy.types.Operator):
    bl_idname = "delete_template_scene.operator"
    bl_label = "Delete Template Scene"
    
    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_all()
        bpy.ops.object.delete()
        
        return {"FINISHED"}          
class ImportMeshData(bpy.types.Operator, ImportHelper):
    bl_idname = "import_mesh.data_operator" 
    bl_label = "Import Mesh"

    filename_ext = "*.fbx;*.obj;"

    filter_glob: StringProperty(
        default="*.fbx;*.obj;",
        options={'HIDDEN'},
        maxlen=255)
        
    def execute(self, context):
        source_path = self.filepath
        extension_split = source_path.split(".")
        if extension_split[1] == "fbx":        
            bpy.ops.import_scene.fbx(filepath=source_path)
        elif extension_split[1] == "obj":
            bpy.ops.import_scene.obj(filepath=source_path)

        return {"FINISHED"}

    
class Help(bpy.types.Operator):
    bl_idname = "help.web_operator"
    bl_label = "Help"
    
    def execute(self, context):
        webbrowser.open("https://www.kaylaman.com/vstitcher2maya-tool.html")
        return {"FINISHED"}
class PBR_SHADER(bpy.types.Operator):
    bl_label = "Create PBR Shader"
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
            if isinstance(k, img)]
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
        
class MAT_CLEARNUP(bpy.types.Operator):
    
    bl_label = "Material Specular Fix"
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
        
        camera_data = bpy.data.cameras.new('camera')
        camera = bpy.data.objects.new('camera', camera_data)
        bpy.context.collection.objects.link(camera)
        
        scene = bpy.context.scene
        scene.camera = camera
        camera.location = (0.0, -10, 0.0)
        camera.rotation_euler = (math.radians(90), 0, 0)
     
        return {"FINISHED"}
    
def updateCam(self,context):
    loc = bpy.context.object.location
    camera = bpy.context.scene.camera
    camera.location[1] = self.distance
    
def updateCamElevation(self,context):
    loc = bpy.context.object.location
    camera = bpy.context.scene.camera
    camera.location[2] = self.elevation
    
class TURNTABLE_SETUP(bpy.types.Operator):
    bl_label = "Turntable Setup"
    bl_idname = "turntable.setup_operator"

    def execute(self, context):
        objects = bpy.context.active_object
        if objects:

            bpy.ops.obejct.empty_add(type = "PLAIN_AXES", align = "WORLD", location = (0,0,0))
            em = bpy.context.object
            objects.parent = em
            objects.matrix_parent_inverse = em.martrix_world.inverted()

            em.rotation_euler[2] = math.radians(0)
            em.keyframe_insert(data_path = "rotation_euler",frame = 1)
            em.rotation_euler[2] = math.radians(360)
            em.keyframe_insert(data_path = "rotation_euler", frame = 120)

            for i in range (0,1):
                frame = em.animation_data.action.fcurves[2].keyframe_points[i]
                frame.interpolation = "LINEAR"
        else:
            self.report({"ERROR"}, "You must select ONE geometry")
            
        return {"FINISHED"}

class DELETE_TURNTABLE(bpy.types.Operator):
    bl_label = "Delete Turntable"
    bl_idname = "delete.turntable_operator"

    def execute(self, context):
        ob = bpy.context.object
        ad = ob.animation_data

        if ad:
            action = ad.action
            if action:
                remove_types = ["rotation"]

                fcurves = [fc for fc in action.fcurves
                            for type in remove_types
                            if fc.data_path.startswith(type)]
                while(fcurves):
                    fc = fcurves.pop()
                    action.fcurves.remove(fc)
                ob.rotation_euler[2] = math.radian(0)
                bpy.data.objects.remove(ob)
            else:
                self.report({"ERROR"}, "No animation data found!")

        return {"FINISHED"}

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
       
class DELHDRI(bpy.types.Operator):
    bl_label = "Delete HDRI"
    bl_idname = "del.hdri_operator"

    def execute(self,context):
        wrd= bpy.data.worlds['World']
        node_del = wrd.node_tree.nodes["Environment Texture"]
        mapping_del = wrd.node_tree.nodes["Mapping"]
        coord_del = wrd.node_tree.nodes["Texture Coordinate"]
            
        wrd.node_tree.nodes.remove( node_del )
        wrd.node_tree.nodes.remove( mapping_del )
        wrd.node_tree.nodes.remove( coord_del )

        return{"FINISHED"}

def setHdriRotation(self, context):
    scn = bpy.context.scene
    world = scn.world
    mapping_node = world.node_tree.nodes["Mapping"]
    
    mapping_node.inputs[2].default_value[2] = math.radians(self.degree)

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
            
class hdriSet(bpy.types.PropertyGroup):
    hdri: StringProperty(
            name="HDRI",
            subtype='FILE_PATH',
            update = updatehdri)
            
    degree: FloatProperty(
            name = "HDRI Rotation",
            subtype="NONE",
            min=0.0, max= 360.0,
            default = 45.0,
            update = setHdriRotation)
            
class camSet(bpy.types.PropertyGroup):
    distance: FloatProperty(
            name = "Zoom In/Out",
            subtype="NONE",
            min = -200.0, max = 200.0,
            default= -10.0,
            update = updateCam)
            
    elevation: FloatProperty(
            name = "Camera Up/Down",
            subtype="NONE",
            min = -200.0, max = 2000.0,
            default = 0.0,
            update = updateCamElevation)
             
def register():
    bpy.utils.register_class(BlendertoVsiticherPanel)
    bpy.utils.register_class(DeleteTemplateScene)
    bpy.utils.register_class(ImportMeshData)
    bpy.utils.register_class(Help)
    bpy.utils.register_class(MAT_CLEARNUP)
    bpy.utils.register_class(CAM_SETUP)
    bpy.utils.register_class(HDRI_MAP)
    bpy.utils.register_class(DELHDRI)
    bpy.utils.register_class(TURNTABLE_SETUP)
    bpy.utils.register_class(DELETE_TURNTABLE)
    bpy.utils.register_class(PBR_SHADER)
    bpy.utils.register_class(materialSet)
    bpy.utils.register_class(hdriSet)
    bpy.utils.register_class(camSet)
    bpy.types.World.my_hdri = PointerProperty(type = hdriSet)
    bpy.types.Object.my_transform = PointerProperty(type = camSet)
    bpy.types.Material.slot_setting=PointerProperty(type=materialSet)
    
def unregister():
    bpy.utils.unregister_class(BlendertoVsiticherPanel)
    bpy.utils.unregister_class(DeleteTemplateScene)
    bpy.utils.unregister_class(ImportMeshData)
    bpy.utils.unregister_class(Help)
    bpy.utils.unregister_class(MAT_CLEARNUP)
    bpy.utils.unregister_class(CAM_SETUP)
    bpy.utils.unregister_class(DELHDRI)
    bpy.utils.unregister_class(HDRI_MAP)
    bpy.utils.unregister_class(TURNTABLE_SETUP)
    bpy.utils.unregister_class(DELETE_TURNTABLE)
    bpy.utils.unregister_class(PBR_SHADER)
    bpy.utils.unregister_class(materialSet)
    bpy.utils.unregister_class(hdriSet)
    bpy.utils.unregister_class(camSet)
    del bpy.types.World.my_hdri
    del bpy.types.Object.my_transform
    del bpy.types.Material.slot_setting
    
if __name__ == "__main__":
    register()