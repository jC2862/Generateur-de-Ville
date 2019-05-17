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
    
    def __init__(self, cell) :
        print(cell)
        #h = HouseGenerator.main() 
        #tranforme une cellule en pseudo-grille (nombre de découpe = 3 pour l instant)
        CellToGrid.fix_face(cell)  
        
        #on selectionne le contour de la grille (contient la face bordure et la ou les aretes de la bordure)
        #(indice face, indice(s) aretes)
        border = CellToGrid.select_boundary_face(cell)
        #print(border)
        #on calcule la rotation de la maison (indice face, angle)
        list = CellToGrid.calc_rotation(cell, border)
        print("###############")
        #pour chq couple de la bordure
        for elt in list :
            print(elt)
            #bpy.ops.object.mode_set(mode = 'OBJECT')
            print("{} : {}".format(elt[0], elt[1]))
            #on creee une maison
            h = HouseGenerator.main() 
            #on calcule la position future de la maison
            pos = CellToGrid.coord_fix(cell ,CellToGrid.get_center_median(cell, elt[0]))
            #print(pos)
            #enfin on deplace et rotate la maison
            CellToGrid.move_and_rotate(h.name, pos, elt[1])
            CellToGrid.scale_percentage(cell, bpy.data.objects[h.name], elt[0])
        
        
        
        
        
def main() :
    work_with = [obj for obj in bpy.context.scene.objects if obj.name.startswith("Plane_cell")]
    list = sample(work_with, 20)        
    
    for cell in list :
        Main(cell)
        
#tmp main to test
#cell = bpy.data.objects['Plane_cell.001_cell.001']
#Main(cell)

#main()