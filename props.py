import bpy
from bpy.props import StringProperty, PointerProperty
from bpy.types import PropertyGroup

class James_Props(PropertyGroup):
    # Đường dẫn thư mục FBX cho tính năng Batch Import
    fbx_dir: StringProperty(
        name="Folder FBX",
        description="Chọn thư mục chứa các file FBX",
        subtype='DIR_PATH',
        default=""
    )

def register():
    bpy.utils.register_class(James_Props)
    # Gắn group vào scene để truy cập qua: context.scene.james_tool
    bpy.types.Scene.james_tool = PointerProperty(type=James_Props)

def unregister():
    bpy.utils.unregister_class(James_Props)
    del bpy.types.Scene.james_tool