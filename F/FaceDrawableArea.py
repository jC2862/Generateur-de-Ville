import bpy
import bmesh
from numpy import abs
from math import pi
from mathutils import Vector

class DrawableArea :
    
    def calc_center_median(self) :
        sum = Vector((0, 0, 0))
        for vert in self.face.verts :
            sum = sum + Vector(vert.co)
        return sum/len(self.face.verts)
    
    #dessine la face interne si elle existe (bientot deprecie)
    def draw(self) :
        if self.rect == None : return -1
        bm = self.mesh
        #ie il y a 52 faces indicees de 0 a 51.
        #donc la prochaine face sera la face 52 ! (il ne faut pas de + 1) 
        index = len(bm.faces)
        
        pt0 = bm.verts.new(self.rect[0])
        pt1 = bm.verts.new(self.rect[1])
        pt2 = bm.verts.new(self.rect[2])
        pt3 = bm.verts.new(self.rect[3])
        bm.verts.ensure_lookup_table()
        
        bm.faces.new([ pt0, pt1, pt2, pt3 ])
        bm.faces.ensure_lookup_table()

        bmesh.update_edit_mesh(bpy.context.object.data)
        #bpy.ops.object.mode_set(mode='OBJECT')
        bm = self.mesh
        print(len(bm.faces))
        self.index_of_next = index
        return index
    
    #rajoute les deux pts manquants pour former un rectangle
    def rect_bl_tr(self, bottom_left, top_right) :
        epsilon = self.epsilon
        pt0 = Vector(bottom_left)
        pt2 = Vector(top_right)
        if 1 - epsilon < self.face.normal[1] <= 1 or -1 <= self.face.normal[1] < -1 + epsilon: 
            pt1 = Vector((top_right[0], bottom_left[1], bottom_left[2]))
            pt3 = Vector((bottom_left[0], bottom_left[1], top_right[2])) 
            return [pt0, pt1, pt2, pt3]
        elif 1 - epsilon < self.face.normal[0] <= 1 or -1 <= self.face.normal[0] < -1 + epsilon :
            pt1 = Vector((bottom_left[0], top_right[1], bottom_left[2]))
            pt3 = Vector((bottom_left[0], bottom_left[1], top_right[2]))
            return [pt0, pt1, pt2, pt3]
    
    def helper(self, top, bottom, left, right) :
        top = abs(top * self.height)
        bottom = abs(bottom * self.height)
        left = abs(left * self.width)
        right = abs(right * self.width)
        return top, bottom, left, right
        
    def get_width_and_height(self) :
        epsilon = self.epsilon
        bottom_left = self.rect[0]
        top_right = self.rect[2]
        width = 0
        height = 0
        if -1 <= self.face.normal[1] < - 1 + epsilon : 
            width = top_right[0] - bottom_left[0]
            height = top_right[2] - bottom_left[2]
        elif 1 - epsilon < self.face.normal[0] <= 1 :   
            width = bottom_left[1] - top_right[1]
            height = top_right[2] - bottom_left[2]
        elif 1 - epsilon < self.face.normal[1] <= 1 :
            width = top_right[0] - bottom_left[0]
            height = top_right[2] - bottom_left[2]
        elif -1 <= self.face.normal[0] < -1 + epsilon :  
            width = bottom_left[1] - top_right[1]
            height = top_right[2] - bottom_left[2] 
        return (width, height)
    
    #creer une representation d'un  quad interne à la face
    def create_inside_rect(self, top, bottom, left, right) : 
        epsilon = self.epsilon
        #on evalue une face // a l axe y
        bottom_left = (0, 0, 0)
        top_right = (0, 0, 0)
        new_bl = (0, 0, 0)
        new_tr = (0, 0, 0)
        if 1 - epsilon < self.face.normal[0] <= 1 or -1 <= self.face.normal[1] < -1 + epsilon :
            print("IF BON COTE")
            bottom_left = ( min(self.face.verts[0].co[0], self.face.verts[2].co[0]),
                            min(self.face.verts[0].co[1], self.face.verts[2].co[1]),
                            min(self.face.verts[0].co[2], self.face.verts[2].co[2])
            )
            top_right = ( max(self.face.verts[0].co[0], self.face.verts[2].co[0]),
                          max(self.face.verts[0].co[1], self.face.verts[2].co[1]),
                          max(self.face.verts[0].co[2], self.face.verts[2].co[2])
            )
            # le x et le z changent : 
            if -1 <= self.face.normal[1] < - 1 + epsilon :
                self.width = top_right[0] - bottom_left[0]
                self.height = top_right[2] - bottom_left[2]
                top, bottom, left, right = self.helper(top, bottom, left, right)
                 
                new_bl = (bottom_left[0] + left, bottom_left[1], bottom_left[2] + bottom)  
                new_tr = (top_right[0] - right, top_right[1], top_right[2] - top)
            # le y et le z changent    
            elif 1 - epsilon < self.face.normal[0] <= 1 :
                print("BL : ", bottom_left)
                print("TR : ", top_right)
                self.width = bottom_left[1] - top_right[1]
                self.height = top_right[2] - bottom_left[2]
                top, bottom, left, right = self.helper(top, bottom, left, right)
                    
                new_bl = (bottom_left[0], bottom_left[1] + left, bottom_left[2] + bottom)  
                new_tr = (top_right[0], top_right[1] - right, top_right[2] - top)
                print("NEW BL : ", new_bl)
                print("NEW TR : ", new_tr)  
        #on evalue une face // a l axe x     
        elif -1 <= self.face.normal[0] < -1 + epsilon or 1 - epsilon < self.face.normal[1] <= 1 :
            print("ELIF MAUVAIS COTE")
            bottom_left = ( max(self.face.verts[0].co[0], self.face.verts[2].co[0]),
                            max(self.face.verts[0].co[1], self.face.verts[2].co[1]),
                            min(self.face.verts[0].co[2], self.face.verts[2].co[2])
            )
            top_right = ( min(self.face.verts[0].co[0], self.face.verts[2].co[0]),
                          min(self.face.verts[0].co[1], self.face.verts[2].co[1]),
                          max(self.face.verts[0].co[2], self.face.verts[2].co[2])
            )
            # le x et le z changent : 
            if 1 - epsilon < self.face.normal[1] <= 1 :
                self.width = top_right[0] - bottom_left[0]
                self.height = top_right[2] - bottom_left[2]
                top, bottom, left, right = self.helper(bottom, top, right, left)
                
                new_bl = (bottom_left[0] - left, bottom_left[1], bottom_left[2] + bottom)  
                new_tr = (top_right[0] + right, top_right[1], top_right[2] - top)
            # le y et le z changent    
            elif -1 <= self.face.normal[0] < -1 + epsilon :
                print("BL : ", bottom_left)
                print("TR : ", top_right)
                self.width = bottom_left[1] - top_right[1]
                self.height = top_right[2] - bottom_left[2]
                top, bottom, left, right = self.helper(top, bottom, left, right)
                print("wtf : {} {} {} {} ".format(top, bottom, left, right))
                    
                new_bl = (bottom_left[0], bottom_left[1] - left, bottom_left[2] + bottom)  
                new_tr = (top_right[0], top_right[1] + right, top_right[2] - top)
                print("NEW BL : ", new_bl)
                print("NEW TR : ", new_tr)  
                    
        rect = self.rect_bl_tr(new_bl, new_tr) 
        print("Si rect existe : ", rect)  
        return rect
    
    def give_offset(self, offset) :
        epsilon = self.epsilon
        bm = self.mesh
        if  bpy.context.object.mode != 'EDIT' :
            print("SHOULD NOT HAPPEN !!!!")
        pos = self.calc_center_median()
        print("-->>>>>POS : ", pos)
        if -1 <= self.face.normal[1] < - 1 + epsilon : 
            pos[1] = pos[1] - offset
        elif 1 - epsilon < self.face.normal[0] <= 1 :   
            pos[0] = pos[0] + offset
        elif 1 - epsilon < self.face.normal[1] <= 1 :
            pos[1] = pos[1] + offset
        elif -1 <= self.face.normal[0] < -1 + epsilon :  
            pos[0] = pos[0] - offset
        return pos    
            
    #apres un self.draw() seulement !!!
    def set_3D_cursor(self) :
        bm = self.mesh
        bm.faces[self.index_of_next].select = True
        #offset un peu le curseur ?
        previous_context = bpy.context.area.type
        bpy.context.area.type = 'VIEW_3D'
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.context.area.type = 'TEXT_EDITOR'
        bpy.context.area.type = previous_context


        
    def set_and_offset_3D_cursor(self, offset) :
        pos = self.give_offset(offset)
        
        previous_context = bpy.context.area.type
        bpy.context.area.type = 'VIEW_3D'
        bpy.context.scene.cursor_location = self.object.matrix_world * pos
        bpy.context.area.type = 'TEXT_EDITOR'
        bpy.context.area.type = previous_context
            
        
    def calc_rotation(self) :
        epsilon = self.epsilon
        if -1 <= self.face.normal[1] < - 1 + epsilon : 
            return 0 * pi/180
        elif 1 - epsilon < self.face.normal[0] <= 1 :   
            return 90 * pi/180
        elif 1 - epsilon < self.face.normal[1] <= 1 :
            return 180 * pi/180
        elif -1 <= self.face.normal[0] < -1 + epsilon :  
            return 270 * pi/180    
    
    #on efface la face de dessin (bientot deprecie)
    def remove_draw_face(self) :
        bm = bmesh.from_edit_mesh(bpy.context.edit_object.data) 
        bm.faces.ensure_lookup_table()
        face = bm.faces[-1]
        bmesh.ops.delete(bm, geom = [face], context = 5)
        bmesh.update_edit_mesh(bpy.context.object.data)
        
    def __init__(self, obj_name, face, top, bottom, left, right) :
        self.epsilon = 0.0002
        self.object = bpy.data.objects[obj_name]
        #on force l'objet actif 
        bpy.context.scene.objects.active = self.object
        bpy.ops.object.mode_set(mode = 'EDIT') 
        me = bpy.context.active_object.data
        bm = bmesh.new()
        bm.from_mesh(me)
        self.mesh = bm
        self.face = face
        self.rect = self.create_inside_rect(top, bottom, left, right)


#top, bottom, left right sont des pourcentages de la face !!!        
#bm = bmesh.from_edit_mesh(bpy.context.edit_object.data) 
#list = bm.faces
#index = -1
#for i in [6] :
#    f = list[i] 
#    print(f.index)    
#    d = DrawableArea(bm, f, 0.2, 0.2, 0.5, 0.1)
    #index = d.draw()
#    d.set_and_offset_3D_cursor(0)
#bm = bmesh.from_edit_mesh(bpy.context.edit_object.data) 
#bm.faces[index].select = True            