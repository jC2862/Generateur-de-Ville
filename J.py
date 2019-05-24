import os
import sys
import imp
import bpy 
from mathutils import Vector

dir_path = os.path.dirname(__file__)
sys.path.append(dir_path+"/J")
import Voronoi
import Utils
import RoadTruc
import Terrain
import CityBorder
import Lsystem
imp.reload(Voronoi)
imp.reload(Utils)
imp.reload(RoadTruc)
imp.reload(Terrain)
imp.reload(CityBorder)
imp.reload(Lsystem)

import bmesh

# fonction pour supprimer de la scène tous les éléments
def cleanAll():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def get_material():
    for mat in bpy.data.materials:
        if mat.name == 'SolBase' :
            return mat
    mat = bpy.data.materials.new(name = 'SolBase')
    mat.use_nodes = True
    
    mat.node_tree.nodes.remove(mat.node_tree.nodes.get('Diffuse BSDF'))
    material_output = mat.node_tree.nodes.get('Material Output')
    toon = mat.node_tree.nodes.new("ShaderNodeBsdfToon")
    
    toon.inputs['Color'].default_value = [0.9,0.6,0.3,1]
    mat.node_tree.links.new(toon.outputs['BSDF'], material_output.inputs["Surface"])
    return mat

def creer_route():
    return Voronoi.execute()

def creer_anim(road):
    RoadTruc.execute(road)

def correct_system(system):
    bpy.ops.view3d.viewnumpad(type = 'TOP')
    bpy.context.scene.tool_settings.use_mesh_automerge = True
    '''
    #bpy.data.scenes["Scene"].tool_settings.snap_element = 'FACE'
    bpy.context.scene.tool_settings.snap_element = 'FACE' 
    bpy.context.scene.tool_settings.use_snap_project = True
    '''
    
    Utils.unselect()
    Utils.select(system)
    bpy.ops.transform.translate(value=(0, 0, 45))
    
    bpy.ops.object.modifier_add(type='SKIN')
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.transform.skin_resize(value=(0.5, 0.5, 0.0001))
    bpy.ops.object.mode_set(mode='OBJECT')   
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Skin")
    
    bpy.ops.object.modifier_add(type='SHRINKWRAP')
    bpy.context.object.modifiers["Shrinkwrap"].target = bpy.data.objects["Terrain"]
    bpy.context.object.modifiers["Shrinkwrap"].wrap_method = 'PROJECT'
    bpy.context.object.modifiers["Shrinkwrap"].use_project_z = True
    bpy.context.object.modifiers["Shrinkwrap"].use_positive_direction = False
    bpy.context.object.modifiers["Shrinkwrap"].use_negative_direction = True
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Shrinkwrap")
    
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, 0.001)})
    bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, 0.01)})
    bpy.ops.object.mode_set(mode='OBJECT')  
    
    system.data.materials.append(get_material())
    
    return


def execute():
    cleanAll()
    T = Terrain
    terrain = T.generation(250, 100)
    center = CityBorder.findPlaceIn(terrain)
    road, cellules = creer_route()
    #creer_anim(road)
    
    bpy.ops.object.select_all(action='DESELECT')
    terrain.select = True
    bpy.ops.transform.translate(value=(-center.x, -center.y, center.z-0.01))
    bpy.ops.object.select_all(action='DESELECT')
    #angle = math.pi/4
    cx = (1 if center.x < 0 else -1)
    cy = (1 if center.y < 0 else -1)
    vec = Vector((10 * cx, 10 * cy))
    dir = Vector((vec.normalized().x, vec.normalized().y))
    system = Lsystem.create(vec, dir, 8)
    bpy.ops.object.select_all(action='DESELECT')
    correct_system(system)
    bpy.ops.object.select_all(action='DESELECT')
    return [road, cellules]
