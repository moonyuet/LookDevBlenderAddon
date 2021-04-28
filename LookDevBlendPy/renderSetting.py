
import bpy

from bpy.props import IntProperty, FloatProperty, PointerProperty, BoolProperty
class RenderSetPanel(bpy.types.Panel):

    bl_label = "Cycles Render Setting Add-On"
    bl_idname = "RENDER_PT_PANEL"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "GPU Render"

    def draw(self, context):
        layout = self.layout
        scn = bpy.context.scene
        row = layout.row()
        row.operator("cycle.gpu_operator")
        row = layout.row()
        layout.label(text="Render Setting")
        row = layout.row()
        row.prop(scn.attr, "x")
        row.prop(scn.attr, "y")
        row = layout.row()
        row.prop(scn.attr, "res")
        row = layout.row()
        row.prop(scn.attr, "rnsample")
        row = layout.row()
        row.prop(scn.attr, "presample")
        row = layout.row()
        row.label(text="Max Bounces for Light Paths")
        row = layout.row()
        row.prop(scn.attr, "maxb")
        row = layout.row()
        row.prop(scn.attr, "difb")
        row.prop(scn.attr, "gloosyb")
        row = layout.row()
        row.prop(scn.attr, "glassb")
        row = layout.row()
        row.prop(scn.attr, "transb")
        row = layout.row()
        row.prop(scn.attr, "vdb")
        row = layout.row()
        row.label(text="Clamping")
        row= layout.row()
        row.prop(scn.attr, "dircl")
        row.prop(scn.attr, "indcl")
        row = layout.row()
        row.prop(scn.attr, "denoise")
        row=layout.row()
        row=layout.label(text="Denoise Parameters")
        row=layout.row()
        row.prop(scn.attr, "radius")
        row=layout.row()
        row.prop(scn.attr, "st")
        row.prop(scn.attr, "st_pr")
        
        
class CYCLE(bpy.types.Operator):

    bl_label = "Cycles Engine in GPU"
    bl_idname = "cycle.gpu_operator"

    def execute(self, context):
        scn = bpy.context.scene
        rn = scn.render
        rn.engine = "CYCLES"
        scn.cycles.device = "GPU"

        return {"FINISHED"}        

def updateRes(self, context):
    render = bpy.context.scene.render
    render.resolution_x = self.x
    render.resolution_y = self.y
    render.resolution_percentage = self.res

def updateSample(self,context):
    scn = bpy.context.scene
    cycles = scn.cycles
    cycles.samples = self.rnsample
    cycles.preview_samples = self.presample

def updateBounces(self,context):
    scn = bpy.context.scene
    cycles = scn.cycles
    cycles.max_bounces = self.maxb
    cycles.diffuse_bounces = self.difb
    cycle.glossy_bounces = self.glossyb
    cycles.transparent_max_bounces = self.glassb
    cycles.transmission_bounces = self.transb
    cycles.volume_bounces = self.vdb

def updateClamp(self,context):
    scn = bpy.context.scene
    cycles = scn.cycles
    cycles.sample_clamp_direct = self.dircl
    cycles.sample_clamp_indirect = self.indcl
    
def updateNoiseFilter(self,context):
    scn = bpy.context.scene
    scn.denoising_radius = self.radius
    scn.use_denoising = self.denoise
    scn.denoising_strength = self.st
    scn.denoising_feature_strength = self.st_pr
    
class ResControlSet(bpy.types.PropertyGroup):

    x: IntProperty(
        name="x",
        subtype="PIXEL",
        min=0, max= 4096,
        default=1920,
        update=updateRes)
    y: IntProperty(
        name="y",
        subtype="PIXEL",
        min=0, max= 4096,
        default= 1080,
        update=updateRes)
    res: IntProperty(
        name="Resolution Percentage",
        subtype="PIXEL",
        min=0, max= 100,
        default=100,
        update=updateRes)
    rnsample: IntProperty(
        name="Render Sampling",
        subtype="NONE",
        min=0, max= 500,
        default=128,
        update=updateSample)
    presample: IntProperty(
        name="Viewport Sampling",
        subtype="NONE",
        min=0, max= 50,
        default=32,
        update=updateSample)
    maxb: IntProperty(
        name="Total",
        subtype="NONE",
        min=0, max= 30,
        default=12,
        update=updateBounces)
    difb: IntProperty(
        name="Diffuse",
        subtype="NONE",
        min=0, max= 30,
        default=4,
        update=updateBounces)
    gloosyb: IntProperty(
        name="Glossy",
        subtype="NONE",
        min=0, max= 30,
        default=4,
        update=updateBounces)
    glassb: IntProperty(
        name="Transparency",
        subtype="NONE",
        min=0, max= 30,
        default=8,
        update=updateBounces)
    transb: IntProperty(
        name="Transmission",
        subtype="NONE",
        min=0, max= 30,
        default=12,
        update=updateBounces)
    vdb: IntProperty(
        name="Volume",
        subtype="NONE",
        min=0, max= 30,
        default=0,
        update=updateBounces)
    dircl: FloatProperty(
        name="Direct Light",
        subtype="NONE",
        min=0.0, max= 10.0,
        default=0,
        update=updateClamp)
    indcl: FloatProperty(
        name="Indirect Light",
        subtype="NONE",
        min=0.0, max= 50.0,
        default=10.0,
        update=updateClamp)
    radius: IntProperty(
        name="Radius",
        subtype="PIXEL",
        min=0, max= 20,
        default=8,
        update=updateNoiseFilter)
    denoise: BoolProperty(
        name="Denoise",
        subtype="NONE",
        default = False,
        update=updateNoiseFilter)
    st: FloatProperty(
        name="Strength",
        subtype="NONE",
        min=0.0, max= 10.0,
        default=0.5,
        update=updateNoiseFilter)
    st_pr: FloatProperty(
        name="Feature Strength",
        subtype="NONE",
        min=0.0, max= 10.0,
        default=0.5,
        update=updateNoiseFilter)
       
def register():
    bpy.utils.register_class(RenderSetPanel)
    bpy.utils.register_class(CYCLE)
    bpy.utils.register_class(ResControlSet)
    bpy.types.Scene.attr = PointerProperty(type=ResControlSet)

def unregister():
    bpy.utils.unregister_class(RenderSetPanel)
    bpy.utils.unregister_class(CYCLE)
    bpy.utils.unregister_class(ResControlSet)
    del bpy.types.Scene.attr 

    
if __name__ == "__main__":
    register()
