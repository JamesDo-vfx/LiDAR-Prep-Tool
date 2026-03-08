import bpy
import os
import shutil

def process_fbx_import(directory, context):
    """
    """
    if not directory or not os.path.exists(directory):
        return "ERROR", "Thư mục không tồn tại!"
    
    fbx_files = [f for f in os.listdir(directory) if f.lower().endswith(".fbx")]
    if not fbx_files: 
        return "WARNING", "Không thấy file FBX nào."
    
    temp_tex_dir = os.path.join(directory, "temp_textures_processing")
    if not os.path.exists(temp_tex_dir):
        os.makedirs(temp_tex_dir)
        
    count = 0
    for fbx_file in fbx_files:
        file_path = os.path.join(directory, fbx_file)
        fbx_name = os.path.splitext(fbx_file)[0]
        bpy.ops.object.select_all(action='DESELECT')
        
        try:
            bpy.ops.import_scene.fbx(filepath=file_path)
            for obj in context.selected_objects:
                if obj.type == 'MESH':
                    obj.name = fbx_name
                    if obj.active_material and obj.active_material.use_nodes:
                        mat = obj.active_material
                        mat.name = f"M_{fbx_name}"
                        for node in mat.node_tree.nodes:
                            if node.type == 'TEX_IMAGE' and node.image:
                                img = node.image
                                old_ext = os.path.splitext(img.filepath)[1] or ".jpg"
                                new_full_name = f"T_{fbx_name}{old_ext}"
                                
                                img.unpack(method='USE_LOCAL') 
                                old_unpacked_path = bpy.path.abspath(img.filepath)
                                new_physical_path = os.path.join(temp_tex_dir, new_full_name)
                                
                                if os.path.exists(old_unpacked_path):
                                    if os.path.exists(new_physical_path):
                                        os.remove(new_physical_path)
                                    shutil.move(old_unpacked_path, new_physical_path)
                                    img.filepath = new_physical_path
                                    img.pack()
                                    img.filepath = f"//textures\\{new_full_name}"

                                img.name = f"T_{fbx_name}"
                                node.label = img.name
            count += 1
        except Exception as e:
            print(f"Lỗi import: {e}")

    if os.path.exists(temp_tex_dir):
        shutil.rmtree(temp_tex_dir)

    return "INFO", f"✅ Đã nhập xong {count} file!"




def process_obj_export_individual(context):
    """
    Xuất OBJ: export / <tên obj> / <obj, mtl, texture>
    """
    blend_path = bpy.data.filepath
    if not blend_path:
        return "ERROR", "Hãy lưu file .blend trước khi xuất!"
    
    basedir = os.path.dirname(blend_path)
# --- BƯỚC 1: XỬ LÝ TEXTURE ---
    export_root = os.path.join(basedir, "export")
    
    selected_objects = [obj for obj in context.selected_objects if obj.type == 'MESH']
    if not selected_objects: 
        return "WARNING", "Hãy chọn Mesh!"

    count = 0
    for obj in selected_objects:
        clean_name = bpy.path.clean_name(obj.name)
        
        # Tạo thư mục riêng cho từng Object bên trong thư mục export
        obj_dir = os.path.join(export_root, clean_name)
        if not os.path.exists(obj_dir):
            os.makedirs(obj_dir)
        
        # --- XỬ LÝ TEXTURE ---
        if obj.active_material and obj.active_material.use_nodes:
            for node in obj.active_material.node_tree.nodes:
                if node.type == 'TEX_IMAGE' and node.image:
                    img = node.image
                    if img.packed_file:
                        img.unpack(method='USE_LOCAL')
                    
                    old_path = bpy.path.abspath(img.filepath)
                    if os.path.exists(old_path):
                        ext = os.path.splitext(old_path)[1] or ".jpg"
                        new_tex_name = f"T_{clean_name}{ext}"
                        target_tex_path = os.path.join(obj_dir, new_tex_name)
                        
                        try:
                            # Copy texture vào đúng thư mục con của object
                            shutil.copy2(old_path, target_tex_path)
                            # Cập nhật đường dẫn tương đối để file .mtl tìm thấy ảnh ngay bên cạnh
                            img.filepath = bpy.path.relpath(target_tex_path, obj_dir)
                        except Exception as e:
                            print(f"Lỗi copy texture: {e}")

# --- BƯỚC 2: THIẾT LẬP SCALE 100 & XUẤT ---
        # Apply Scale để dữ liệu Mesh thực sự lớn lên (quan trọng cho OBJ)
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        context.view_layer.objects.active = obj
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

        filepath_obj = os.path.join(obj_dir, f"{clean_name}.obj")
        
        # Tiến hành xuất
        bpy.ops.wm.obj_export(
            filepath=filepath_obj,
            export_selected_objects=True,
            export_materials=True,
            path_mode='RELATIVE'
        )
                
        count += 1

    message = f"✅ Đã xuất {count} file (Scale x100) vào /export/!"
    context.workspace.status_text_set_internal(message)
    return "INFO", message