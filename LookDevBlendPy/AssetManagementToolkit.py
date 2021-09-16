import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty

class AssetManagementToolkitPanel(bpy.types.Panel):
    bl_label = "Asset Management Toolkit"
    bl_idname = "MESH_PT_PANEL"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Asset Management"

    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.operator("delete_template_scene.operator")
        
        row = layout.row()
        row.operator("import_asset.operator")
        row.operator("fitscenesize.operator")

        row = layout.row()
        row.operator("importcamerascene.operator")
        
        row = layout.row()
        row.operator("importlightscene.operator")

class DeleteTemplateScene(bpy.types.Operator):
    bl_idname = "delete_template_scene.operator"
    bl_label = "Delete Template Scene"

    def execute(self, context):
        bpy.ops.object.select_all(action="DESELECT")
        bpy.ops.object.select_all()
        bpy.ops.object.delete()

        return{"FINISHED"}

class ImportAsset(bpy.types.Operator, ImportHelper):
    bl_idname = "import_asset.operator"
    bl_label = "Import Asset"

    filename_ext = "*obj;"

    filter_glob: StringProperty(
        default = "*obj;",
        options = {"HIDDEN"},
        maxlen = 255)

    def execute(self, context):
        source_path = self.filepath
        bpy.ops.import_scene.obj(filepath=source_path)

        return {"FINISHED"}
    
class FitSceneSize(bpy.types.Operator):
    bl_idname = "fitscenesize.operator"
    bl_label = "Fit Scene Size"
    
    def execute(self, context):
        obj = bpy.context.active_object
        obj.scale = (0.01, 0.01, 0.01)
        
        return {"FINISHED"}    

class CameraTemplate(bpy.types.Operator, ImportHelper):
    bl_idname = "importcamerascene.operator"
    bl_label = "Import Camera Scene"

    filename_extension = "*blend;"
    filter: StringProperty(
        default = "*blend;",
        options = {"HIDDEN"},
        maxlen = 255)
    
    def execute(self, context):
        source_path = self.filepath
        with bpy.data.libraries.load(source_path, link=False) as (data_from, data_to):
            data_to.objects = [name for name in data_from.objects if name.startswith("Camera")]
        for obj in data_to.objects:
            if obj is not None:
                bpy.context.collection.objects.link(obj)
                
        s_data = bpy.context.space_data
        s_data.use_local_camera = True
        s_data.camera = obj
        
        scn = bpy.context.scene
        scn.render.engine = "CYCLES"   
        scn.render.resolution_x = 2048
        scn.render.resolution_y = 2048
        
        return {"FINISHED"}

class LightTemplate(bpy.types.Operator,ImportHelper):
    bl_idname = "importlightscene.operator"
    bl_label = "Import Light Scene"

    filename_extension = "*blend;"
    filter: StringProperty(
        default = "*blend;",
        options = {"HIDDEN"},
        maxlen = 255)
    
    def execute(self, context):
        source_path = self.filepath
        with bpy.data.libraries.load(source_path, link=False) as (data_from, data_to):
            data_to.objects = [name for name in data_from.objects if name.endswith("light")]
        for obj in data_to.objects:
            if obj is not None:
                bpy.context.collection.objects.link(obj)
                   
        return {"FINISHED"}
    
def register():
    bpy.utils.register_class(AssetManagementToolkitPanel)
    bpy.utils.register_class(DeleteTemplateScene)
    bpy.utils.register_class(ImportAsset)
    bpy.utils.register_class(FitSceneSize)
    bpy.utils.register_class(CameraTemplate)
    bpy.utils.register_class(LightTemplate)

def unregister():
    bpy.utils.unregister_class(AssetManagementToolkitPanel)
    bpy.utils.unregister_class(DeleteTemplateScene)
    bpy.utils.unregister_class(ImportAsset)
    bpy.utils.unregister_class(FitSceneSize)
    bpy.utils.unregister_class(CameraTemplate)
    bpy.utils.unregister_class(LightTemplate)

if __name__ == "__main__":
    try:
        unregister()
    except:
        pass
    register()