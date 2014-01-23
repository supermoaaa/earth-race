# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Mass Renamer",
    "author": "Timothée Lhuillier",
    "version": (1, 0),
    "blender": (2, 6, 9),
    "location": "View3D > Toolbar > Rename",
    "description": "Mass renaming of objects",
    "warning": "",
    "category": "Object"}


import bpy
from bpy.props import *


class MassRenamer(bpy.types.Operator):
    bl_idname = "mass_renamer.rename"
    bl_label = "Mass renaming of objects"
    
    def execute(self, context):
        obs = context.selected_editable_objects
        obs = sorted(obs, key=lambda ob: ob.name)
        iFormat = '0' + str(int(len(obs) / 10)) + 'd'
        for i, ob in enumerate(obs):
            ob.name = context.window_manager.mass_renamer.prefix + format(i, iFormat)
        return {'FINISHED'}


class MassSwitch(bpy.types.Operator):
    bl_idname = "mass_renamer.switch"
    bl_label = "Mass switch name of objects"
    
    def execute(self, context):
        obs = context.selected_editable_objects
        obs = sorted(obs, key=lambda ob: ob.name)
        obsNames = [ob.name for ob in obs]
        for i, ob in enumerate(obs[:int(len(obs)/2)]):
            j = len(obs) - i - 1
            obs[j].name = "tmpNameMassSwitch"
            ob.name = obsNames[j]
            obs[j].name = obsNames[i]
        return {'FINISHED'}


class MassRenamerProps(bpy.types.PropertyGroup):
    prefix = StringProperty(name='Prefix Name',
                            default='New Name',
                            description='Rename all with this String')

class ToolsPanel(bpy.types.Panel):
    bl_label = "Rename"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
 
    def draw(self, context):
        #context.window_manager.mass_renamer = MassRenamerProps()
        #prefix = StringProperty(name='Prefix Name',
        #                               default='New Name',
        #                               description='Rename all with this String')
        self.layout.prop(context.window_manager.mass_renamer, 'prefix')
        self.layout.operator("mass_renamer.rename")
        self.layout.operator("mass_renamer.switch")

def register():
    bpy.utils.register_module(__name__)
    bpy.types.WindowManager.mass_renamer = bpy.props.PointerProperty(\
        type=MassRenamerProps)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == '__main__':
    register()
