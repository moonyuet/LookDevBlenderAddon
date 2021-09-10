import bpy
import math
class TurntablePanel(bpy.types.Panel):
    
    bl_label = "Turntable Addon"
    bl_idname = "TURNTABLE_PT_PANEL"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "TUrntable"
    
    def draw(self, context):
        layout = self.layout
        layout.row()
        layout.operator("turntable.setup_operator")
        layout.row()
        layout.operator("delete.turntable_operator")

class TURNTABLE_SETUP(bpy.types.Operator):
    bl_label = "Turntable setup"
    bl_idname = "turntable.setup_operator"
    
    def execute(self, context):
        
        objects = bpy.context.active_object
        if objects:
                
            empty = bpy.ops.object.empty_add(type= "PLAIN_AXES", align='WORLD', location = (0,0,0))
            em = bpy.context.object
            objects.parent = em
            objects.matrix_parent_inverse = em.matrix_world.inverted()

            em.rotation_euler[2] = math.radians(0)
            em.keyframe_insert(data_path="rotation_euler", frame=1)
            em.rotation_euler[2] = math.radians(360)
            em.keyframe_insert(data_path="rotation_euler", frame=120)

            for i in range (0, 1):
                frame = em.animation_data.action.fcurves[2].keyframe_points[i]
                frame.interpolation = 'LINEAR'
        else:
            self.report({"ERROR"}, "You must select ONE geometry.")
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
                # select all that have datapath above
                fcurves = [fc for fc in action.fcurves
                        for type in remove_types
                        if fc.data_path.startswith(type)]
                # remove fcurves
                while(fcurves):
                    fc = fcurves.pop()
                    action.fcurves.remove(fc)
                ob.rotation_euler[2] = math.radians(0)
                bpy.data.objects.remove(ob)
            else:
                self.report({"ERROR"}, "No animation data needed")

        return {"FINISHED"}
def register():
    bpy.utils.register_class(TurntablePanel)
    bpy.utils.register_class(TURNTABLE_SETUP)
    bpy.utils.register_class(DELETE_TURNTABLE)

def unregister():
    bpy.utils.unregister_class(TurntablePanel)
    bpy.utils.unregister_class(TURNTABLE_SETUP)
    bpy.utils.unregister_class(DELETE_TURNTABLE)



if __name__ == "__main__":
    register()
            
#TODO: allows users to customize the frame 
    