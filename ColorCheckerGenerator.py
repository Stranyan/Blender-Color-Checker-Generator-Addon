# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Color Checker",
    "author" : "Taya", 
    "description" : "Color Checker",
    "blender" : (3, 0, 0),
    "version" : (1, 0, 1),
    "location" : "",
    "warning" : "",
    "doc_url": "", 
    "tracker_url": "", 
    "category" : "3D View" 
}

import bpy
import bpy.utils.previews
import bmesh
import numpy as np

addon_keymaps = {}
_icons = None

def panel(self, context):
    if not (False):
        layout = self.layout
        op = layout.operator('sna.op_generator', text='Color Checker', icon_value=859, emboss=True, depress=False)

class sna_op_generator(bpy.types.Operator):
    bl_idname = "sna.op_generator"
    bl_label = "Operator"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def colorchecker(self, context):
        color_list = [[252,252,252],
                    [44,56,142],
                    [249,118,35],
                    [115, 82, 69],
                    [230,230,230],
                    [74,148,81],
                    [80,91,182],
                    [204, 161, 141],
                    [200,200,200],
                    [179,42,50],
                    [222,91,125],
                    [101, 134, 179],
                    [143,143,142],
                    [250,226,21],
                    [91,63,123],
                    [89, 109, 61],
                    [100,100,100],
                    [191,81,160],
                    [173,232,91],
                    [141,137,194],
                    [50,50,50],
                    [6,142,172],
                    [255,164,26],
                    [132,228,208]]

        color_list_slash = np.divide(color_list, 255)

        b = np.array(color_list_slash)

        bpy.ops.mesh.primitive_plane_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        for obj in bpy.context.selected_objects:
            obj.name = "ColorChecker"
            obj.data.name = "ColorChecker_Mesh"
            
        bpy.ops.object.modifier_add(type='ARRAY')
        bpy.context.object.modifiers["Array"].count = 4
        bpy.context.object.modifiers["Array"].relative_offset_displace[0] = 1.2
        bpy.ops.object.modifier_add(type='ARRAY')
        bpy.context.object.modifiers["Array.001"].count = 6
        bpy.context.object.modifiers["Array.001"].relative_offset_displace[0] = 0
        bpy.context.object.modifiers["Array.001"].relative_offset_displace[1] = -1.2

        bpy.ops.object.apply_all_modifiers()

        bpy.context.object.scale[1] = 0.1
        bpy.context.object.scale[2] = 0.1
        bpy.context.object.scale[0] = 0.1
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        bpy.context.object.show_in_front = True

        bpy.ops.object.mode_set(mode='EDIT')
        obj = bpy.context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)

        n = 0

        while n < 24:
            bpy.ops.object.mode_set(mode='EDIT')
            obj = bpy.context.edit_object
            me = obj.data
            bm = bmesh.from_edit_mesh(me)
            bm.faces.ensure_lookup_table()
            bpy.ops.mesh.select_all(action='DESELECT')
            bm.faces[n].select = True  
            bpy.ops.object.mode_set(mode='VERTEX_PAINT')
            bpy.context.object.data.use_paint_mask = True
            bpy.data.brushes["Draw"].color = (color_list_slash[n])
            bpy.ops.paint.vertex_color_set()
            n = n + 1

        bpy.ops.object.mode_set(mode='EDIT')
        bmesh.update_edit_mesh(me)
        bpy.ops.object.mode_set(mode='OBJECT')

        ob = bpy.context.active_object
        mat = bpy.data.materials.get("ColorChecker_Material")
        if mat is None:
            mat = bpy.data.materials.new(name="ColorChecker_Material")
        if ob.data.materials:
            ob.data.materials[0] = mat
        else:
            ob.data.materials.append(mat)
        mat.use_nodes = True
        bpy.data.materials["ColorChecker_Material"].node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0
        bpy.data.materials["ColorChecker_Material"].node_tree.nodes["Principled BSDF"].inputs[9].default_value = 1
        bpy.data.materials["ColorChecker_Material"].node_tree.nodes["Principled BSDF"].inputs[13].default_value = 0
        material = bpy.data.materials.get("ColorChecker_Material")
        nodes = material.node_tree.nodes
        attribute_node = nodes.new(type = 'ShaderNodeAttribute')
        lightpath_node = nodes.new(type = 'ShaderNodeLightPath')
        tr_node = nodes.new(type = 'ShaderNodeBsdfTransparent')
        mix_node = nodes.new(type = 'ShaderNodeMixShader')
        bpy.data.materials["ColorChecker_Material"].node_tree.nodes["Attribute"].attribute_name = "Col"
        material.node_tree.links.new(nodes["Principled BSDF"].inputs[0], attribute_node.outputs[0])
        material.node_tree.links.new(lightpath_node.outputs[1], mix_node.inputs[0])
        material.node_tree.links.new(nodes["Principled BSDF"].outputs[0], mix_node.inputs[1])
        material.node_tree.links.new(tr_node.outputs[0], mix_node.inputs[2])
        material.node_tree.links.new(nodes["Material Output"].inputs[0], mix_node.outputs[0])
        bpy.context.object.active_material.shadow_method = 'NONE'
        bpy.context.object.active_material.diffuse_color = (0.75, 0.5, 0.25, 1) 

        bpy.ops.object.constraint_add(type='LIMIT_ROTATION')
        bpy.context.object.constraints["Limit Rotation"].use_limit_x = True
        bpy.context.object.constraints["Limit Rotation"].use_limit_y = True

        bpy.ops.object.constraint_add(type='COPY_ROTATION')

        camera = bpy.data.scenes["Scene"].camera
        if camera is None:
            bpy.ops.object.camera_add()
            for obj in bpy.context.selected_objects:
                obj.name = "ColorChecker_Camera"
                obj.data.name = "ColorChecker_CameraMesh"
            bpy.context.scene.camera = bpy.data.objects["ColorChecker_Camera"]
        camera = bpy.data.scenes["Scene"].camera
        bpy.data.objects["ColorChecker"].constraints["Copy Rotation"].target = camera
        bpy.data.objects["ColorChecker"].constraints["Copy Rotation"].mix_mode = 'BEFORE'
        
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.colorchecker(context)
    
def register():
    global _icons
    _icons = bpy.utils.previews.new()
    bpy.types.VIEW3D_MT_editor_menus.append(panel)
    bpy.utils.register_class(sna_op_generator)

def unregister():
    global _icons
    bpy.utils.previews.remove(_icons)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    for km, kmi in addon_keymaps.values():
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    bpy.types.VIEW3D_MT_editor_menus.remove(panel)
    bpy.utils.unregister_class(sna_op_generator)
