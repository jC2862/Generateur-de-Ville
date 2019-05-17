import bpy
import bmesh
import sys
import os
from random import sample, randint, uniform

#HouseGenerator est temporaire
IMPORTS = ["FaceDrawableArea.py", "Window.py"] 
dir_path = os.path.dirname(os.path.realpath(__file__))
for im in IMPORTS:
    print(dir_path+"/"+im)
    sys.path.append(dir_path+"/"+im)
import FaceDrawableArea, Window

class WindowGenerator :
    
    def __init__(self, house) :
        self.house = house
        # nombre maximal de murs sur lesquels on veut pouvoir dessiner une fenetre
        max_available_walls = len(self.house.architecture['walls_face_id']) - 1
        #on ne veux pas forcement dessiner sur tous ces 5 murs, on laisse
        # l aleatoire decider pour nous
        k = randint(1, max_available_walls)
        #choisit k murs parmi tous nos murs
        self.occupied_walls = sample(self.house.architecture['walls_face_id'], k)
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
            top = uniform(0.05, 0.1)
            bottom = uniform(0.4, 0.55)
            left = uniform(0.05, 0.2)
            right = uniform(0.05, 0.2)
            bm.faces.ensure_lookup_table()
            #DrawableArea('nom', bm.faces[wall], top, bottom, left, right)
            face_draw = FaceDrawableArea.DrawableArea(self.house.name, bm.faces[wall], top, bottom, left, right)
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
            win = Window.Window(self.house, bm.faces[draw_area.face.index], dimension[0]/2, dimension[1]/2, thickness)
            win.draw_basic(rot)
     
#house = HouseGenerator.main()           
#wG = WindowGenerator(house)     
    