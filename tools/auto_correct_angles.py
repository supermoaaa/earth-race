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
	"name": "AutoCorrect Angles",
	"author": "Timothée Lhuillier",
	"version": (1, 0),
	"blender": (2, 6, 9),
	"location": "View3D > Toolbar > AutoCorrect Angles",
	"description": "Correct the angles for the empty used by cars in earth-race to place and oriente the wheels",
	"warning": "",
	"category": "Object"}


import bpy
from bpy.props import *


class AutoCorrectAngles(bpy.types.Operator):
	bl_idname = "auto_correct_angles.auto_correct"
	bl_label = "Auto Correct Angles"

	def execute(self, context):
		obs = context.selected_editable_objects
		for ob in obs:
			if ob.scale[0]<0 and ob.scale[1]<0 and ob.scale[2]<0:
				corrected = False
				for i in range(0,3):
					if not corrected and 3.141593<ob.rotation_euler[i]<3.141594:
						ob.rotation_euler[i] = 0
						corrected = i
					else:
						ob.scale[i] = -ob.scale[i]
		return {'FINISHED'}

class AutoCorrectAnglesPanel(bpy.types.Panel):
	bl_label = "AutoCorrect Angles"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"

	def draw(self, context):
		self.layout.operator("auto_correct_angles.auto_correct")

def register():
	bpy.utils.register_module(__name__)

def unregister():
	bpy.utils.unregister_module(__name__)

if __name__ == '__main__':
	register()
