import bpy
import bmesh
import sys
import os
from mathutils import Vector
from random import random, randint, uniform

IMPORTS = ["HouseTypeA.py", "HouseTypeB.py", "F\_Utils.py"] 
dir_path = os.path.dirname(os.path.realpath(__file__))
for im in IMPORTS:
    print(dir_path+"/"+im)
    sys.path.append(dir_path+"/"+im)
import HouseTypeA, HouseTypeB, F_Utils

#Faut jouer un peu avec les intervales 
def generateRandomHouse() :
    type = randint(0, 1)
    #type = 1
    if type == 0 :
            # params
            # height, width, length, roof_width
            height = randint(1, 3)
            width = randint(2, 7)
            length = randint(2, 7)
            roof_height = randint(1, 8)
            roof_width = 1
            # nota bene la tranformation trop swag ne se fait pas avec des doubles !!!!
            house = HouseTypeA.House(height, width, length, roof_height, roof_width)
            return house
    elif type == 1 :
            # params : 
            # height, width_front, length_front, width_L, length_L, roof_height, roof_width
            height = randint(1, 3)
            width_front = randint(2, 7)
            length_front = randint(5, 14)
            width_L = randint(2, length_front - 1)
            length_L = width_front + randint(1, 14)
            roof_height = randint(1, 8)
            roof_width = uniform(0, 1)
            print("h : {}\nw_f : {}\nl_f : {}\nw_L : {}\nl_L : {}\nr_h : {}".format(height, width_front, length_front, width_L, length_L, roof_height))
            house = HouseTypeB.House(height, width_front, length_front, width_L, length_L, roof_height, roof_width)
            return house
    
def main() :
    #   F_Utils.clean_Current()
    if bpy.context.mode != 'OBJECT' :
        bpy.ops.object.mode_set(mode = 'OBJECT') 
    previous_context = bpy.context.area.type
    print(previous_context)
    bpy.context.area.type = 'VIEW_3D'
    bpy.ops.view3d.snap_cursor_to_center()
    bpy.context.area.type = 'TEXT_EDITOR'
    bpy.context.area.type = previous_context

    h = generateRandomHouse()
    bpy.context.object.scale[0] = 0.8
    bpy.context.object.scale[1] = 0.8
    bpy.context.object.scale[2] = 0.8
    bpy.ops.object.mode_set(mode = 'OBJECT') 
    #bpy.ops.mesh.select_all(action = 'DESELECT')
    return h

#main()

def move_to(coord_x, coord_y) :
    if bpy.context.mode != 'OBJECT' :
        bpy.ops.object.mode_set(mode = 'OBJECT') 
    bpy.ops.object.select_all(action='TOGGLE')
    h = generateRandomHouse()
    #h est toujours l'objet actif
    obj = bpy.context.active_object
    obj.location = obj.location + Vector((coord_x, coord_y, 0))
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT') 
    return h

#main()
#HOTFIX : bpy.ops.object.origin_set(type = 'ORIGIN_GEOMETRY')
#ou autre car z pose pbm (pour les maisons en forme de L)
#move_to(0, 0)
#move_to(15, 0)
#move_to(0, 15)
#move_to(15, 15)