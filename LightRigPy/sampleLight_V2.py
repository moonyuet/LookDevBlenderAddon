bl_info ={
    "name": "Material Creation",
    "author" : "Kayla Man",
    "version" : (1,0),
    "blender" : (2,91,0),
    "location" : " ",
    "description" : "creating light rig in Blender",
    "warning": "", 
    "wiki_url": "",
    "category": "Light Rig"
}
import bpy
from bpy.props import FloatProperty, FloatVectorProperty, PointerProperty
class LightSetPanel(bpy.types.Panel):

    bl_label = "Lighting Rig Add-On"
    bl_idname = "LIGHT_PT_PANEL"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Light Rig"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        layout.label(text="Standard Light Rig")
        row =layout.row()
        layout.label(text="Front=8,Rim=10,Key=12,Back=16")
        row = layout.row()
        row.operator("light.rig_operator")
        ob = bpy.context.scene
        row=layout.row()
        row.prop(ob.light_rig,"color")
        row=layout.row()
        row.prop(ob.light_rig, "intensity")
        row=layout.row()
        row.prop(ob.light_rig, "scale")
        

class LIGHT_RIG(bpy.types.Operator):

    bl_label = "4-Point Light Rig"
    bl_idname = "light.rig_operator"

    def execute(self, context):
        #rimlight
        rlight = bpy.data.lights.new(name ="rimlight", type="AREA")
        rlight.energy = 10
        rlit_obj = bpy.data.objects.new(name = "rimlight", object_data = rlight)

        bpy.context.collection.objects.link(rlit_obj)
        bpy.context.view_layer.objects.active = rlit_obj

        rlit_obj.location =(-1, 0, 1.07)
        rlit_obj.rotation_euler = (3.14159, 1.5708, 0)
        rlit_obj.scale = (5, 5, 1)

    
        #frontlight
        flight = bpy.data.lights.new(name="frontlight", type="AREA")
        flight.energy = 8
        flit_obj = bpy.data.objects.new(name = "frontlight", object_data = flight)

        bpy.context.collection.objects.link(flit_obj)
        bpy.context.view_layer.objects.active = flit_obj

        flit_obj.location = (0, -1.3, 1.03)
        flit_obj.rotation_euler = (1.5708, 1.5708, 0)
        flit_obj.scale = (5, 5, 1)

        #keylight
        klight = bpy.data.lights.new(name="keylight", type="AREA")
        klight.energy = 12
        klit_obj = bpy.data.objects.new(name="keylight", object_data = klight)

        bpy.context.collection.objects.link(klit_obj)
        bpy.context.view_layer.objects.active = klit_obj

        klit_obj.location = (1, 0, 1.07)
        klit_obj.rotation_euler = (0, 1.5708, 0)
        klit_obj.scale = (5, 5, 1)

        #backlight

        blight = bpy.data.lights.new(name="backlight", type="AREA")
        blight.energy = 16
        blit_obj = bpy.data.objects.new(name="backlight", object_data = blight)

        bpy.context.collection.objects.link(blit_obj)
        bpy.context.view_layer.objects.active = blit_obj

        blit_obj.location = (0, 1.5, 1.03)
        blit_obj.rotation_euler = (-1.5708, 1.5708, 0)
        blit_obj.scale = (5, 5, 1)

        return {'FINISHED'}
    
def updateIntensity(self,context):
    obj = bpy.context.active_object
    light = obj.data
    light.energy = self.intensity
    light.color = self.color
    obj.scale[0]= self.scale
    obj.scale[1]= self.scale

class LightParamSet(bpy.types.PropertyGroup):

    intensity: FloatProperty(
        name="Intensity",
        subtype="POWER",
        min=0, max= 12,
        update = updateIntensity)
    
    color : FloatVectorProperty(
        name="Light Color",
        subtype="COLOR",
        default=(1,1,1),
        update = updateIntensity)
    scale: FloatProperty(
        name="Scale",
        subtype="NONE",
        default=5,
        min=1, max= 100,
        update = updateIntensity)

def register():
    bpy.utils.register_class(LightSetPanel)
    bpy.utils.register_class(LIGHT_RIG)
    bpy.utils.register_class(LightParamSet)
    bpy.types.Scene.light_rig = PointerProperty(type=LightParamSet)



def unregister():
    bpy.utils.unregister_class(LightSetPanel)
    bpy.utils.unregister_class(LIGHT_RIG)
    bpy.utils.unregister_class(LightParamSet)
    del bpy.types.Scene.light_rig 
    
if __name__ == "__main__":
    register()

