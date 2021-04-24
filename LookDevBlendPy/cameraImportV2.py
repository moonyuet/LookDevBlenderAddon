import bpy
bl_info ={
    "name": "Camera",
    "author" : "Kayla Man",
    "version" : (1,0),
    "blender" : (2,91,0),
    "location" : " ",
    "description" : "creating cameras in Blender",
    "warning": "", 
    "wiki_url": "",
    "category": "Camera"
}
import bpy
from bpy.props import PointerProperty, BoolProperty
class CameraSetPanel(bpy.types.Panel):

    bl_label = "Camera Creation Add-On"
    bl_idname = "CAMERA_PT_PANEL"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Camera"

    def draw(self, context):
        layout = self.layout
        da = bpy.context.scene
        row = layout.row()
        row.operator("frn.cambuild_operator")
        row = layout.row()
        row.operator("left.cambuild_operator")
        row = layout.row()
        row.operator("right.cambuild_operator")
        row = layout.row()
        row.operator("back.cambuild_operator")
        row = layout.row()
        row.prop(da.myCamView, "lock")

class FRN_CAM(bpy.types.Operator):

    bl_label = "Front Camera"
    bl_idname = "frn.cambuild_operator"

    def execute(self, context):

        frn_cam = bpy.data.cameras.new("Front Camera")
        cam_obI = bpy.data.objects.new("Front Camera", frn_cam)
        cam_obI.location = (0, -0.8, 0.96)
        cam_obI.rotation_euler = (1.5708,0,0)
        bpy.context.collection.objects.link(cam_obI)
        return {"FINISHED"}


class LEFT_CAM(bpy.types.Operator):

    bl_label = "Left Camera"
    bl_idname = "left.cambuild_operator"

    def execute(self, context):

        left_cam = bpy.data.cameras.new("Left Camera")
        cam_obII = bpy.data.objects.new("Left Camera", left_cam)
        cam_obII.location = (1.5, 0, 0.96)
        cam_obII.rotation_euler = (1.5708,0, 1.5708)
        bpy.context.collection.objects.link(cam_obII)
        return {"FINISHED"}

class RIGHT_CAM(bpy.types.Operator):

    bl_label = "Right Camera"
    bl_idname = "right.cambuild_operator"

    def execute(self, context):

        right_cam = bpy.data.cameras.new("Right Camera")
        cam_obIII = bpy.data.objects.new("Right Camera", right_cam)
        cam_obIII.location = (-1.5, 0, 0.96)
        cam_obIII.rotation_euler = (1.5708,0, -1.5708)
        bpy.context.collection.objects.link(cam_obIII)
        return {"FINISHED"}

class BACK_CAM(bpy.types.Operator):

    bl_label = "Back Camera"
    bl_idname = "back.cambuild_operator"

    def execute(self, context):

        back_cam = bpy.data.cameras.new("Back Camera")
        cam_obIV = bpy.data.objects.new("Back Camera", back_cam)
        cam_obIV.location = (0, 0.8, 0.96)
        cam_obIV.rotation_euler = (-1.5708, 3.14159, 0)
        bpy.context.collection.objects.link(cam_obIV)
        return {"FINISHED"}
    
def lockCameraToView(self,context):
    da = bpy.context.space_data
    da.lock_camera= self.lock
    
class CAMDRIVENSET(bpy.types.PropertyGroup):
    lock: BoolProperty(
        name="Lock Camera To View",
        subtype="NONE",
        default = False,
        update=lockCameraToView)


def register():
    bpy.utils.register_class(CameraSetPanel)
    bpy.utils.register_class(FRN_CAM)
    bpy.utils.register_class(LEFT_CAM)
    bpy.utils.register_class(RIGHT_CAM)
    bpy.utils.register_class(BACK_CAM)
    bpy.utils.register_class(CAMDRIVENSET)
    bpy.types.Scene.myCamView = PointerProperty(type=CAMDRIVENSET)

def unregister():
    bpy.utils.unregister_class(CameraSetPanel)
    bpy.utils.unregister_class(FRN_CAM)
    bpy.utils.unregister_class(LEFT_CAM)
    bpy.utils.unregister_class(RIGHT_CAM)
    bpy.utils.unregister_class(BACK_CAM)
    bpy.utils.unregister_class(CAMDRIVENSET)
    del bpy.types.Scene.myCamView
 
if __name__ == "__main__":
    register()
