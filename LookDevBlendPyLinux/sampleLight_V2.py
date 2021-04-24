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
        row.prop(ob.light_rig, "scale")
        row=layout.row()
        row.prop(ob.light_rig,"bckCol")
        row=layout.row()
        row.prop(ob.light_rig, "bckintensity")
        row=layout.row()
        row.prop(ob.light_rig,"frnCol")
        row=layout.row()
        row.prop(ob.light_rig, "frnintensity")
        row=layout.row()
        row.prop(ob.light_rig,"keyCol")
        row=layout.row()
        row.prop(ob.light_rig, "keyintensity")
        row=layout.row()
        row.prop(ob.light_rig,"rimCol")
        row=layout.row()
        row.prop(ob.light_rig, "rimintensity")
        
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
    lamp_objects = [o for o in bpy.data.objects
                if o.type == 'LIGHT']
                
    lamp_objects[0].data.energy = self.bckintensity
    lamp_objects[0].data.color = self.bckCol
    lamp_objects[1].data.energy = self.frnintensity
    lamp_objects[1].data.color = self.frnCol
    lamp_objects[2].data.energy = self.keyintensity
    lamp_objects[2].data.color = self.keyCol
    lamp_objects[3].data.energy = self.rimintensity
    lamp_objects[3].data.color = self.rimCol
    #TODO:make attributes for each lighting
    for o in lamp_objects:
        o.scale[0]= self.scale
        o.scale[1]= self.scale
        

class LightParamSet(bpy.types.PropertyGroup):

    bckintensity: FloatProperty(
        name="Back Light Intensity",
        subtype="POWER",
        default= 16,
        min=0, max= 100,
        update = updateIntensity)
    
    bckCol: FloatVectorProperty(
        name="Back Light Color",
        subtype="COLOR",
        default=(1,1,1),
        update = updateIntensity)
        
    frnintensity: FloatProperty(
        name="Front Light Intensity",
        subtype="POWER",
        default= 8,
        min=0, max= 100,
        update = updateIntensity)
    
    frnCol: FloatVectorProperty(
        name="Front Light Color",
        subtype="COLOR",
        default=(1,1,1),
        update = updateIntensity)
    
    keyintensity: FloatProperty(
        name="Key Light Intensity",
        subtype="POWER",
        default= 12,
        min=0, max= 100,
        update = updateIntensity)
    
    keyCol: FloatVectorProperty(
        name="Key Light Color",
        subtype="COLOR",
        default=(1,1,1),
        update = updateIntensity)
    
    rimintensity: FloatProperty(
        name="Rim Light Intensity",
        subtype="POWER",
        default= 10,
        min=0, max= 100,
        update = updateIntensity)
    
    rimCol: FloatVectorProperty(
        name="Rim Light Color",
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

