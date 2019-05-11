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
            length_front = randint(4, 14)
            width_L = randint(2, length_front   )
            length_L = width_front + randint(1, 14)
            roof_height = randint(1, 8)
            roof_width = uniform(0, 1)
            print("h : {}\nw_f : {}\nl_f : {}\nw_L : {}\nl_L : {}\nr_h : {}".format(height, width_front, length_front, width_L, length_L, roof_height))
            house = HouseTypeB.House(height, width_front, length_front, width_L, length_L, roof_height, roof_width)
            return house
    
def main() :
    #   F_Utils.clean_Current()
    h = generateRandomHouse()
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT') 
    return 0

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
    return 0