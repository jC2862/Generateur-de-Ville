import bpy
import bmesh
import sys
import os
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
            #y a un truc a fixer pour ca je crois
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
            roof_width = 1
            print("h : {}\nw_f : {}\nl_f : {}\nw_L : {}\nl_L : {}\nr_h : {}".format(height, width_front, length_front, width_L, length_L, roof_height))
            house = HouseTypeB.House(height, width_front, length_front, width_L, length_L, roof_height, roof_width)
            return house
    
def main() :
	# ne marche pas
    # F_Utils.clean_Current()
    h = generateRandomHouse()
    return 0   