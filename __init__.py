bl_info = {
    "name": "LidarScan for MatchMove",
    "author": "JamesDo",
    "version": (1 , 0),
    "blender": (4, 5, 0),
    "location": "View3D > Sidebar > James Tools",
    "description": "Specially designed for aligning and synchronizing raw 3D scans before importing them into MatchMove software",
    "category": "Import-Export",
}

import bpy
from . import props, operators

def register():
    props.register()
    operators.register()

def unregister():
    operators.unregister()
    props.unregister()