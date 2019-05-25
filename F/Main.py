import bpy
import bmesh
import os
import sys
from math import ceil
from random import sample, randint, uniform

IMPORTS = ["HouseGenerator.py", "CellToGrid.py", "Sky.py"] 
dir_path = os.path.dirname(os.path.realpath(__file__))
for im in IMPORTS:
    print(dir_path+"/"+im)
    sys.path.append(dir_path+"/"+im)
import HouseGenerator, CellToGrid, Sky

class Main :
    
    def __init__(self, cell, nb) :
        print(cell)
        #h = HouseGenerator.main() 
        #tranforme une cellule en pseudo-grille (nombre de découpe = 3 pour l instant)
        #CellToGrid.fix_face(cell.data)  
        grid = CellToGrid.Cell_To_Grid(cell, nb_subdivision = nb)
        grid.make_grid()
        
        print(grid.work_area)
        #on selectionne le contour de la grille (contient la face bordure et la ou les aretes de la bordure)
        #(indice face, indice(s) aretes)
        border = CellToGrid.select_boundary_face(grid.work_area)
        #on calcule la rotation de la maison (indice face, angle)
        rotation = grid.calc_rotation(border)
        print(rotation)
        skip = 0
        for elt in rotation :
            if uniform(0, 1) > 0.7 :
                break
            #    continue
            #skip = skip + 1
            h = HouseGenerator.main() 
            pos = CellToGrid.coord_fix(cell ,CellToGrid.get_center_median(grid.work_area, elt[0]))
            #print(pos)
            #enfin on deplace et rotate la maison
            CellToGrid.move_and_rotate(bpy.data.objects[h.name], pos, elt[1])
            CellToGrid.scale_percentage(grid.work_area, bpy.data.objects[h.name], elt[0])
        
        
        
def main(selected_list) :
    
    scene = bpy.context.scene

    # Create new lamp datablock
    lamp_data = bpy.data.lamps.new(name="Sun", type='SUN')

    # Create new object with our lamp datablock
    lamp_object = bpy.data.objects.new(name="Sun", object_data=lamp_data)

    # Link lamp object to the scene so it'll appear in this scene
    scene.objects.link(lamp_object)
    
    # Place lamp to a specified location
    lamp_object.location = (5.0, 5.0, 5.0)
    
    #lamp_object.data.node_tree.nodes['Emission'].inputs['Strength'].default_value = 2

    #args optionnels : color, turbidity, albedo
    Sky.main()
   
    #rd = randint(ceil(len(select)/2), len(select)) 
    #print(rd)
    #print(len(select))
    #sp = set(sample(select, rd))
    
    for cell in selected_list :
        #la subdivision minimale fait une taille de 1, elle se fera même si on passe un 0 !
        Main(bpy.data.objects[cell], nb = randint(0, 1))
        
#tmp main to test
#cell = bpy.data.objects['Plane_cell.001_cell.001']
#Main(cell)

#main()