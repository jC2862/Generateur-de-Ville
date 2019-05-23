import bpy
import bmesh
import os
import sys
from random import uniform, sample
from math import sqrt
from numpy import dot, cross, array, matrix, identity

IMPORTS = ["FaceDrawableC.py", "F_Utils.py", "Material.py"] 
dir_path = os.path.dirname(os.path.realpath(__file__))
for im in IMPORTS:
    print(dir_path+"/"+im)
    sys.path.append(dir_path+"/"+im)
import FaceDrawableC, F_Utils, Material

region, rv3d, v3d, area = F_Utils.view3d_find(True)

override = {
    'scene'  : bpy.context.scene,
    'region' : region,
    'area'   : area,
    'space'  : v3d
}

class Door :
    
    #ici la face n'appartient pas vraiment au mesh 'house', c'est une face que l on aura créé à partir           d'une autre
    def __init__(self, house, face, width, height, thickness) :
        self.house = house
        self.face = face
        self.width = width
        self.height = height
        self.thickness = thickness
        
    def draw_basic(self, offset, rotation) :
        #On dessine directment au bon endroit !!!!
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.mesh.primitive_cube_add()
        
        bpy.context.object.data.name = self.house.obj_name + 'Door'
        bpy.context.object.name = self.house.name + '_Door'
        
        #on sauvegarde le nom de la maison pour identifier le mesh qui lui correspond !
        self.obj_name = bpy.context.object.data.name
        self.name = bpy.context.object.name
        obj = bpy.data.objects[self.name]
        Material.affect_mat(obj, self.name + "_Door_mat", 'Frame')
        bpy.context.object.active_material_index = 0
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.transform.resize(value = (self.width, self.thickness, 0), constraint_axis = (True, True, False))
        bpy.ops.mesh.select_all(action='DESELECT')    
        bpy.ops.object.mode_set(mode='OBJECT')
        for i in [0,2, 4, 6] :
            obj.data.vertices[i].co[2] = obj.data.vertices[i].co[2] - self.house.height * 0.75
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.transform.translate(value=(0, 0, -offset), constraint_axis=(False, False, True))
        bpy.ops.mesh.select_all(action='DESELECT')  
        bpy.ops.object.mode_set(mode='OBJECT')  
        bpy.ops.transform.rotate(value=rotation, axis=(0,0,1), constraint_axis=(False, False, True))
        
class DoorGenerator :
          
    def __init__(self, house, available) :
        self.house = house
        #choisit k murs parmi tous nos murs
        self.occupied_walls = sample(available, 1)
        self.free_walls = set(available) - set(self.occupied_walls)
        obj = bpy.data.objects[self.house.name]
        #on force l'objet courant
        bpy.context.scene.objects.active = obj
        bpy.ops.object.mode_set(mode = 'EDIT')
        me = bpy.context.active_object.data
        bm = bmesh.new()
        bm.from_mesh(me)
        drawable_faces = self.init_face_drawable_area(bm)  
        self.the_works(bm, drawable_faces)
        bm.to_mesh(me)
        bm.free()        
    
    def init_face_drawable_area(self, bm) : 
        drawable_faces = []   
        for wall in self.occupied_walls :
            top = 0.2
            left = .2
            right = .5
            bm.faces.ensure_lookup_table()
            #DrawableArea('nom', bm.faces[wall], top, bottom, left, right)
            face_draw = FaceDrawableC.DrawableArea(self.house.name, bm.faces[wall], top, left, right)
            drawable_faces.append(face_draw)      
        return drawable_faces   
    
     #nom temporaire
    def the_works(self, bm, drawable_faces) :
        for draw_area in drawable_faces :
            thickness = uniform(0.05, 0.1)
            dimension = draw_area.get_width_and_height()
            draw_area.set_and_offset_3D_cursor(thickness/2)
            rot = draw_area.calc_rotation()
            
            bm.faces.ensure_lookup_table()
            #machin machin width height thickness
            doa = Door(self.house, bm.faces[draw_area.face.index], dimension[0]/2, dimension[1], thickness)
            doa.draw_basic(abs(draw_area.rect[0][2]),rot)     
            print("FFS :", rot)
                 