import bpy

from bpy.props import IntProperty, FloatProperty, PointerProperty, BoolProperty
class CPURenderBPTPanel(bpy.types.Panel):

    bl_label = "Cycles Render Setting Add-on 2"
    bl_idname = "RENDER_PT_PANEL"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "CPU Render"
    
    def draw(self,context):
        
        layout = self.layout
        scn = bpy.context.scene
        row = layout.row()
        row.operator("cycle.cpubpt_operator")
        row = layout.row()
        layout.label(text="Render Setting")
        row = layout.row()
        row.prop(scn.param, "x")
        row.prop(scn.param, "y")
        row = layout.row()
        row.prop(scn.param, "res")
        row = layout.row()
        row.label(text="Sampling")
        row = layout.row()
        row.prop(scn.param, "rnsample")
        row = layout.row()
        row.prop(scn.param, "presample")
        row = layout.row()
        row.label(text="Sub Samples")
        row = layout.row()
        row.prop(scn.param, "dif_samp")
        row.prop(scn.param, "gloss_samp")
        row = layout.row()
        row.prop(scn.param, "trans_samp")
        row = layout.row()
        row.prop(scn.param, "ao_samp")
        row.prop(scn.param, "mhli_samp")
        row=layout.row()
        row.prop(scn.param, "ss_samp")
        row.prop(scn.param, "vol_samp")
        row = layout.row()
        row.label(text="Max Bounces for Light Paths")
        row = layout.row()
        row.prop(scn.param, "maxb")
        row = layout.row()
        row.prop(scn.param, "difb")
        row.prop(scn.param, "gloosyb")
        row = layout.row()
        row.prop(scn.param, "glassb")
        row = layout.row()
        row.prop(scn.param, "transb")
        row = layout.row()
        row.prop(scn.param, "vdb")
        row = layout.row()
        row.label(text="Clamping")
        row = layout.row()
        row.prop(scn.param, "dircl")
        row = layout.row()
        row.prop(scn.param, "indcl")
        row = layout.row()
        row.prop(scn.param, "denoise")
        row = layout.row()
        row.prop(scn.param, "radius")
        row = layout.row()
        row.prop(scn.param, "st")
        row = layout.row()
        row.prop(scn.param, "st_pr")

class CYCLEBPT(bpy.types.Operator):
    
    bl_label = "Cycles Engine in CPU (BPT)"
    bl_idname = "cycle.cpubpt_operator"
    
    def execute(self,context):
        
        scn = bpy.context.scene
        rn = scn.render
        rn.engine = "CYCLES"
        scn.cycles.device = "CPU"
        scn.cycles.progressive = "BRANCHED_PATH"

        return {"FINISHED"}

def updateRes(self, context):
    
    render = bpy.context.scene.render
    render.resolution_x = self.x
    render.resolution_y = self.y
    render.resolution_percentage = self.res

def updateSample(self,context):
    
    scn = bpy.context.scene
    cycles = scn.cycles
    cycles.aa_samples = self.rnsample
    cycles.preview_aa_samples = self.presample

def updateSubSample(self,context):
    
    scn = bpy.context.scene
    cycles = scn.cycles
    cycles.diffuse_samples = self.dif_samp
    cycles.glossy_samples = self.gloss_samp
    cycles.transmission_samples = self.trans_samp
    cycles.ao_samples = self.ao_samp
    cycles.mesh_light_samples = self.mhli_samp
    cycles.subsurface_samples = self.ss_samp
    cycles.volume_samples = self.vol_samp

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

class CPUResControlSet(bpy.types.PropertyGroup):
    
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
    dif_samp: IntProperty(
        name="Diffuse",
        subtype="NONE",
        min=0, max= 30,
        default=1,
        update=updateSubSample)
    gloss_samp: IntProperty(
        name="Glossy",
        subtype="NONE",
        min=0, max= 30,
        default=1,
        update=updateSubSample)
    trans_samp: IntProperty(
        name="Transmission",
        subtype="NONE",
        min=0, max= 30,
        default=1,
        update=updateSubSample)
    ao_samp: IntProperty(
        name="AO",
        subtype="NONE",
        min=0, max= 30,
        default=1,
        update=updateSubSample)
    mhli_samp: IntProperty(
        name="Mesh Light",
        subtype="NONE",
        min=0, max= 30,
        default=1,
        update=updateSubSample)
    ss_samp: IntProperty(
        name="SSS",
        subtype="NONE",
        min=0, max= 30,
        default=1,
        update=updateSubSample)
    vol_samp: IntProperty(
        name="Volume",
        subtype="NONE",
        min=0, max= 30,
        default=1,
        update=updateSubSample)
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
    bpy.utils.register_class(CPURenderBPTPanel)
    bpy.utils.register_class(CYCLEBPT)
    bpy.utils.register_class(CPUResControlSet)
    bpy.types.Scene.param = PointerProperty(type = CPUResControlSet)

def unregister():    
    bpy.utils.unregister_class(CPURenderBPTPanel)
    bpy.utils.unregister_class(CYCLEBPT)
    del bpy.types.Scene.param

if __name__ == "__main__":
    register()
