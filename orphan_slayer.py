# orphan_slayer.py (c) 2011 Phil Cote (cotejrp1)
#
# ***** BEGIN GPL LICENSE BLOCK *****
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****

bl_info = {
    'name': 'Orphan Slayer',
    'author': 'Phil Cote, cotejrp1, (http://www.blenderaddons.com)',
    'version': (0,1),
    "blender": (2, 5, 9),
    "api": 35853,
    'location': 'VIEW 3D -> TOOLS',
    'description': 'Deletes objects from a scene and from the bpy.data modules',
    'warning': '', # used for warning icon and text in addons panel
    'category': 'System'}

import bpy, random, time
from pdb import set_trace

    
class DeleteSceneObsOp(bpy.types.Operator):
    '''Remove all objects from the scene..'''
    bl_idname = "ba.delete_scene_obs"
    bl_label = "Delete Scene Objects"

    def execute(self, context):
        for ob in context.scene.objects:
            context.scene.objects.unlink(ob)
        return {'FINISHED'}


class DeleteOrphansOp(bpy.types.Operator):
    '''Remove all orphaned objects of a selected type from the project.'''
    bl_idname="ba.delete_data_obs"
    bl_label="Delete Orphans"
    
    def execute(self, context):
        target = context.scene.mod_list
        target_coll = eval("bpy.data." + target)
        
        num_deleted = 0
        
        for item in target_coll:
            if item.users == 0:
                target_coll.remove(item)
                num_deleted += 1
        
        msg = "Removed %d orphaned %s objects" % (num_deleted, target)
        self.report( { 'INFO' }, msg  )
        return {'FINISHED'}
    

class OrphanSlayerPanel( bpy.types.Panel ):
    
    bl_label = "Orphan Slayer"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    
    def draw( self, context ):
        scn = context.scene
        layout = self.layout
        new_col = self.layout.column
        
        new_col().column().prop(scn, "mod_list")
        new_col().column().operator("ba.delete_data_obs")
        new_col().separator()
        new_col().column().operator("ba.delete_scene_obs")
    

def register():

    mod_data = [tuple(["actions"]*3), tuple(["armatures"]*3), 
                 tuple(["cameras"]*3), tuple(["curves"]*3),
                 tuple(["fonts"]*3), tuple(["grease_pencil"]*3),
                 tuple(["groups"]*3), tuple(["images"]*3),
                 tuple(["lamps"]*3), tuple(["lattices"]*3),
                 tuple(["libraries"]*3), tuple(["materials"]*3),
                 tuple(["meshes"]*3), tuple(["metaballs"]*3),
                 tuple(["node_groups"]*3), tuple(["objects"]*3),
                 tuple(["sounds"]*3), tuple(["texts"]*3), 
                 tuple(["textures"]*3),]
    
    
    bpy.types.Scene.mod_list = bpy.props.EnumProperty(name="Target", 
                                                        items=mod_data, 
                                                        description="Module choice made for orphan deletion")
    bpy.utils.register_class(DeleteSceneObsOp)
    bpy.utils.register_class(DeleteOrphansOp)
    bpy.utils.register_class(OrphanSlayerPanel)
    

def unregister():
    bpy.utils.unregister_class(DeleteSceneObsOp)
    bpy.utils.unregister_class(DeleteOrphansOp)
    bpy.utils.unregister_class(OrphanSlayerPanel)


if __name__ == "__main__":
    register()