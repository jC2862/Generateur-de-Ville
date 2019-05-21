import bpy
import bmesh
import os
import sys
from random import sample

IMPORTS = ["HouseGenerator.py", "CellToGrid.py"] 
dir_path = os.path.dirname(os.path.realpath(__file__))
for im in IMPORTS:
    print(dir_path+"/"+im)
    sys.path.append(dir_path+"/"+im)
import HouseGenerator, CellToGrid

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
            if skip % 2 == 0 :
                skip = skip + 1
                continue
            skip = skip + 1
            h = HouseGenerator.main() 
            pos = CellToGrid.coord_fix(cell ,CellToGrid.get_center_median(grid.work_area, elt[0]))
            #print(pos)
            #enfin on deplace et rotate la maison
            CellToGrid.move_and_rotate(bpy.data.objects[h.name], pos, elt[1])
            CellToGrid.scale_percentage(grid.work_area, bpy.data.objects[h.name], elt[0])
        
        
        
def main() :
    work_with = [obj for obj in bpy.context.scene.objects if obj.name.startswith("Plane_cell")]
    sp = sample(work_with, 1)        
    
    for cell in sp :
        Main(cell, nb = 2)
        
#tmp main to test
#cell = bpy.data.objects['Plane_cell.001_cell.001']
#Main(cell)

main()