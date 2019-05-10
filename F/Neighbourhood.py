import bpy
import bmesh
import sys
import os

#add "\F" to the path in final git build
IMPORTS = ["HouseGenerator.py"] 
dir_path = os.path.dirname(os.path.realpath(__file__))
for im in IMPORTS:
    print(dir_path+"/"+im)
    sys.path.append(dir_path+"/"+im)
import HouseGenerator


class Neighbourhood :
    
    #une grille de n * m maisons
    def __init__(self, grp_n, grp_m) :
        self.grp_size = (grp_n, grp_m)
        
    def create_neighbourhood(self) :
        coord_offset = (25, 25)
        obj_list = []
        for i in range(0, self.grp_size[0]) :
            for j in range(0, self.grp_size[1]) :
                #fct qui cree une maison et la déplace
                house = HouseGenerator.move_to(i * coord_offset[0], j * coord_offset[1])
                obj = bpy.context.active_object
                obj_list.append(obj)   
                
        return obj_list 
    
    #crée un grp nomme grp_name, si grp_name existe deja alosr 'grp_name'.001 ...etc
    def to_group(self, grp_name, list) :
        groups = bpy.data.groups
        group = groups.get(grp_name, groups.new(grp_name))
        for obj in list:
            if obj.name not in group.objects:
                group.objects.link(obj)
