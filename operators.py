import bpy
import textwrap
import os
from . import methods  

# --- 1. UI PANEL ---
class VIEW3D_PT_MM_Multicam_Final(bpy.types.Panel):
    bl_label = "JamesDo's Scan Aligner"
    bl_idname = "VIEW3D_PT_mm_multicam_final"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'LidarScan for MatchMove'

    # Internal function to wrap text (auto line break) 🌷
    def draw_help_text(self, layout, text, icon='NONE'):
        wrapper = textwrap.TextWrapper(width=35)
        lines = wrapper.wrap(text=text)
        for i, line in enumerate(lines):
            layout.label(text=line, icon=icon if i == 0 else 'NONE')

    def draw(self, context):
        layout = self.layout
        scene = context.scene 
        
        # --- SECTION 1: IMPORT ---

        box = layout.box()
        col = box.column(align=True)
        col.label(text="1. Import Raw Lidar Scan", icon='IMPORT')
        
        note_col = col.column(align=True)
        note_col.scale_y = 0.8
        self.draw_help_text(note_col, "Naming: <Shot>_<Sequence>.fbx", icon='INFO')

        col.separator()
        col.operator("object.batch_fbx_import_rename", text="Batch Import Scan", icon='FILE_NEW')
        
        layout.separator()

        # --- SECTION 2: SCENE REGISTRATION (ALIGN TOOL) ---

        box = layout.box()
        col = box.column(align=True)
        col.label(text="2. Scene Registration", icon='SNAP_GRID')

        note_col = col.column(align=True)
        note_col.scale_y = 0.8
        self.draw_help_text(note_col, "Set Origin -> Cursor 0 -> Snap Obj -> Apply All.", icon='LIGHT')

        col.separator()
        # Set Pivot to Cursor
        col.operator("object.origin_set", text="Origin to 3D Cursor", icon='CURSOR').type = 'ORIGIN_CURSOR'
        # Snap object to Cursor location
        col.operator("view3d.snap_selected_to_cursor", text="Selection to Cursor", icon='SNAP_GRID').use_offset = False

        col.separator()

        # Snap Cursor to World Origin (0,0,0)
        col.operator("view3d.snap_cursor_to_center", text="Cursor to World Origin", icon='WORLD')
        
        col.separator()

        # Apply All Transforms
        op = col.operator("object.transform_apply", text="Apply All Transforms", icon='CHECKMARK')
        op.location = True; op.rotation = True; op.scale = True

        layout.separator()

        # --- SECTION 3: EXPORT ---

        box = layout.box()
        col = box.column(align=True)
        col.label(text="3. Export Aligned Model", icon='EXPORT')
        col.prop(scene, "use_3de_scale_100", text="Scale 100 (For MatchMove Software)")
        col.separator()
        col.operator("object.batch_obj_export_rename", text="Export Mesh", icon='EXPORT')

        layout.separator()

        # --- SECTION 4: AUTHOR ---
        col_author = layout.column(align=True)
        col_author.label(text="Author: JamesDo", icon='USER')
        
        # Social links row centered 🌷✨
        row = col_author.row(align=True)
        row.alignment = 'CENTER'
        row.scale_y = 1.2
        
        # Link icons (Using safe system icons)
        row.operator("wm.url_open", text="", icon='QUESTION').url = "https://your-wiki-link.com"  # Wiki
        row.operator("wm.url_open", text="", icon='SCRIPT').url = "https://github.com/JamesDo-vfx"     # Github
        row.operator("wm.url_open", text="", icon='URL').url = "https://jamesdo-vfx.github.io/JamesDo-Portfolio/"      # Portfolio
        row.operator("wm.url_open", text="", icon='COMMUNITY').url = "https://www.facebook.com/jamesdo.vfx/" # Facebook

# --- 2. OPERATORS ---

class BATCH_OT_fbx_import(bpy.types.Operator):
    bl_idname = "object.batch_fbx_import_rename"
    bl_label = "Batch Import FBX"
    bl_description = "Batch import FBX files and automatically handle naming/textures"
    directory: bpy.props.StringProperty(subtype="DIR_PATH")
    
    def execute(self, context):
        try:
            res, msg = methods.process_fbx_import(self.directory, context)
            self.report({res}, msg)
        except Exception as e:
            self.report({'ERROR'}, f"Import Error: {str(e)}")
        return {'FINISHED'}
        
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class BATCH_OT_obj_export(bpy.types.Operator):
    bl_idname = "object.batch_obj_export_rename"
    bl_label = "Export for MatchMove SOFTWARE"
    bl_description = "Export selected meshes as OBJ to the 'export' folder."
    
    def execute(self, context):
        if not context.selected_objects:
            self.report({'WARNING'}, "Please select at least one Mesh to export! 🌷")
            return {'CANCELLED'}
            
        try:
            is_scale_100 = context.scene.use_3de_scale_100
            res, msg = methods.process_obj_export_individual(context, use_scale_100=is_scale_100)
            self.report({res}, msg)
        except Exception as e:
            self.report({'ERROR'}, f"Export Error: {str(e)}")
        return {'FINISHED'}


# --- 3. REGISTRATION ---
classes = (
    BATCH_OT_fbx_import,
    BATCH_OT_obj_export,
    VIEW3D_PT_MM_Multicam_Final,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # Register scene property for the checkbox 🌷
    bpy.types.Scene.use_3de_scale_100 = bpy.props.BoolProperty(
        name="Scale 100 for 3DE",
        description="Enable to automatically scale up by 100 on export",
        default=True
    )

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    if hasattr(bpy.types.Scene, "use_3de_scale_100"):
        del bpy.types.Scene.use_3de_scale_100

if __name__ == "__main__":
    register()