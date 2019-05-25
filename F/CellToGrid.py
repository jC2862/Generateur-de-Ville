import bpy
import bmesh
from random import uniform
from math import sqrt, atan2, pi, degrees
from mathutils import Vector
from numpy import dot, cross, clip, arccos
from numpy.linalg import norm

def unit_vector(vector):
    #renvoie le vecteur unitaire
    if norm(vector) == 0 : return Vector((0, -1, 0))
    return vector / norm(vector)

def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return arccos(clip(dot(v1_u, v2_u), -1.0, 1.0))

#coord globales
def coord_fix(object, vertex) :
    return object.matrix_world * vertex

def dist_fix(edge) :
    obj = bpy.context.active_object.data
    r_edge = obj.edges[edge]
    pt0 = obj.vertices[r_edge.vertices[0]].co
    pt1 = obj.vertices[r_edge.vertices[1]].co
    return sqrt( (pt1[0] - pt0[0]) ** 2
                +(pt1[1] - pt0[1]) ** 2
                +(pt1[2] - pt0[2]) ** 2
                )    
    
def sortDist(edge) :
    return dist_fix(edge)

#Pas utilisé ?
def average_length(cell) :
    sum = 0.0
    for edge in cell.edges :
        sum = sum + dist_fix(edge)
    return sum / len(cell.edges)        

#renvoie (face index, [edges index])
def select_boundary_face(obj) :
    bpy.context.scene.objects.active = obj
    print("DEBUG", obj)
    print("DEBUG", bpy.context.mode)
    if bpy.context.mode != 'EDIT' :
        bpy.ops.object.mode_set(mode = 'EDIT') 
    bm = bmesh.from_edit_mesh(obj.data)
    #nom pas top :/ 
    res = []
    for face in bm.faces :
        edge_border = []
        for edge in face.edges :
            if edge.is_boundary :
                edge_border.append(edge.index)
        if len(edge_border) > 0 :
            res.append((face.index, edge_border))
            #face.select = True
                       
    return res 

def get_center_median(object, face) :
    save = bpy.context.scene.objects.active
    print("save :", save) 
    bpy.context.scene.objects.active = object
    print("A ce stade :", bpy.context.scene.objects.active)
    bpy.ops.object.mode_set(mode = 'EDIT')
    bm = bmesh.from_edit_mesh(object.data)
    sum = Vector((0, 0, 0))
    bm.faces.ensure_lookup_table()
    for vert in bm.faces[face].verts :
        #print("sommets : {}, coord {}".format(vert.index, vert.co))     
        sum = sum + vert.co
    #print("faces :", sum)
    bpy.context.scene.objects.active = save
    return sum / len(bm.faces[face].verts) 

def get_center_edge(object, edges) :
    bpy.context.scene.objects.active = object
    bm = bmesh.from_edit_mesh(object.data)
    sum = Vector((0, 0, 0))
    list_verts = []
    bm.edges.ensure_lookup_table()
    for edge in edges :
        for vert in bm.edges[edge].verts :     
            list_verts.append(vert)
    t_list = list(dict.fromkeys(list_verts))
    #print(t_list)       
    for vert in t_list :
        sum = sum + vert.co
    #print("edge : ", sum)        
    return sum / len(t_list) 
    
    
def move_and_rotate(object, dest, rot) :
    save = bpy.context.scene.objects.active 
    bpy.ops.mesh.select_all(action='DESELECT')   
    bpy.context.scene.objects.active = object
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.context.scene.objects.active.location = dest
    bpy.context.scene.objects.active.rotation_euler = (0, 0, rot)
    bpy.context.scene.objects.active = save
    #bpy.ops.transform.rotate(value=rot, axis=(0, 0, 1), constraint_axis=(False, False, True))
  
#########################################################################  
def dist(pt0, pt1) :
    return sqrt( (pt1[0] - pt0[0]) ** 2 
                +(pt1[1] - pt0[1]) ** 2
                +(pt1[2] - pt0[2]) ** 2
                )

def get_bounding_box_area(obj_name) :
    #house.name
    obj = bpy.data.objects[obj_name]
    pt0 = (obj.bound_box[0][0], obj.bound_box[0][1], obj.bound_box[0][2]) 
    pt1 = (obj.bound_box[3][0], obj.bound_box[3][1], obj.bound_box[3][2])
    pt2 = (obj.bound_box[4][0], obj.bound_box[4][1], obj.bound_box[4][2])
    h = dist(pt0, pt1)
    (h)
    l = dist(pt0, pt2)
    (l)
    area = h * l
    #aire au sol
    return area 
 
######################################################################### 
   
def scale_percentage(cell, object, face) :
    bpy.ops.object.mode_set(mode = 'EDIT')
    bound_area = get_bounding_box_area(object.name)
    
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.context.scene.objects.active = cell
    bpy.ops.object.mode_set(mode = 'EDIT')
    bm = bmesh.from_edit_mesh(cell.data) 
    
    bm.faces.ensure_lookup_table()
    face_area = bm.faces[face].calc_area()
    scale = sqrt((bound_area / face_area))
    print("SCALEEEEEEEEEEEE : ", scale)

    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.scene.objects.active = object
    print("scale of house : {} {} {}".format(object.scale[0], object.scale[1], object.scale[2]))
    object.scale[0] = min((object.scale[0] / (scale)) * 2, 0.3) 
    object.scale[1] = min((object.scale[1] / (scale)) * 2, 0.3)
    object.scale[2] = min((object.scale[2] / (scale)) * 2, 0.3)
    print("scale of house POST: {} {} {}".format(object.scale[0], object.scale[1], object.scale[2]))
    
    res_1, res_2, res_3 = object.dimensions
    if object.dimensions[0] < 2.5 or object.dimensions[0] > 3 :
            res_1 = uniform(2, 2.5)
    if object.dimensions[1] < 2.5 or object.dimensions[1] > 3 :
            res_2 = uniform(2, 2.5)
    if object.dimensions[2] < 3 or object.dimensions[2] > 4:
            res_3 = uniform(3,3.6)
    object.dimensions = [res_1, res_2, res_3]
        
#bm = bmesh.from_edit_mesh(bpy.context.active_object.data)
#obj = bpy.context.active_object.data
#fix_face(obj) 
#res = select_boundary_face(obj)
#list = calc_rotation(res)
#print(list)


def get_area(object) :
    ex_active = bpy.context.scene.objects.active
    ex_active.select = False
    bpy.ops.object.mode_set(mode='OBJECT')
    #nouvel objet actif :
    bpy.context.scene.objects.active = object
    #on veut juste calculer l'aire de cet objet
    mode = object.mode
    bpy.ops.object.mode_set(mode='EDIT')
    print(object.mode)
    bm = bmesh.from_edit_mesh(bpy.context.scene.objects.active.data)
    
    sum = 0.0
    for face in bm.faces :
        sum = sum + face.calc_area()
    
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.scene.objects.active = ex_active    
    return sum
#on passe en global parce que c est cool le global
#center_face = coord_fix(get_center_median(list[0][0]))
#house = bpy.data.objects['House']
#move_and_rotate(house, center_face, list[0][1])
#scale_percentage('House', 0)

class Cell_To_Grid :
    
    def calc_rotation(self, border) :
        bpy.ops.object.mode_set(mode = 'EDIT')
        list = []
        for elt in border : 
            #center_face = get_center_median(self.work_area, elt[0])
            center_edge = get_center_edge(self.work_area, elt[1])
            
            print("face N°{} : target  {}".format(elt[0], center_edge))
            list.append((elt[0], self.get_angle((center_edge))))
        #
        #target = Vector((0, 0, 0))
        return list 
    
    def get_angle(self, to) :
        center = self.get_cell_grid_center(self.work_area)
        local = center[0]
        vec_0 = Vector((0, -1, 0)) - local
        vec_1 = Vector(to) - local 
        sign = 1
        if vec_1[0] < vec_0[0] :
            sign = -1 
        
        print("VEc 1 :", vec_1)
        print("Moi :", angle_between(vec_0, vec_1))
        #print("angle() :",vec_0.angle(vec_1))
        print("HOPE : ", (sign * angle_between(vec_0, vec_1) * 180/pi ))
        return sign * angle_between(vec_0, vec_1)
            
    def make_grid(self) :
        print("Start")
        bpy.context.scene.objects.active = self.work_area
        if bpy.context.mode != 'EDIT' :
            bpy.ops.object.mode_set(mode = 'EDIT')
        bm = bmesh.from_edit_mesh(self.work_area.data)
        if len(bm.verts) == 4 and self.sub == 0:
            return 
        if len(bm.verts) > 4 :
            list = []
            #les plus petites aretes sont en premier
            for edge in bm.edges :
                list.append(edge.index)
            list.sort(key = sortDist)
            
            bpy.ops.mesh.select_all(action='DESELECT')
            #on va merger en leur centres les aretes les plus petites afin d'obtenir un quad
            #approximant la cellule
           
            stop = len(list) - 4
            print(list[:stop])
            bpy.ops.object.mode_set(mode = 'OBJECT')
            for elt in list[:stop] :
                self.work_area.data.edges[elt].select = True
            
            bpy.ops.object.mode_set(mode = 'EDIT')     
            bpy.ops.mesh.merge(type='COLLAPSE')
            
            bm = bmesh.from_edit_mesh(self.work_area.data)
            bm.faces.ensure_lookup_table()
        bpy.ops.mesh.select_all(action='SELECT')    
        bpy.ops.mesh.subdivide(number_cuts = self.sub)
        bpy.ops.mesh.region_to_loop()
        print("end")
    
    def get_area(self, object) :
        ex_active = bpy.context.scene.objects.active
        ex_active.select = False
        bpy.ops.object.mode_set(mode='OBJECT')
        #nouvel objet actif :
        bpy.context.scene.objects.active = object
        #on veut juste calculer l'aire de cet objet
        mode = object.mode
        bpy.ops.object.mode_set(mode='EDIT')
        print(object.mode)
        bm = bmesh.from_edit_mesh(bpy.context.scene.objects.active.data)
        
        sum = 0.0
        for face in bm.faces :
            sum = sum + face.calc_area()
        
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.scene.objects.active = ex_active    
        return sum
    
    #object est soit self.base_obj soit self.work_area
    def get_cell_grid_center(self, object) :
        object.update_from_editmode()
        selection = [vert.co for vert in object.data.vertices]
        
        pivot = sum(selection, Vector()) / len(selection)

        print("Local:", pivot)
        print("Global:", object.matrix_world * pivot)
        return (pivot, object.matrix_world * pivot)
        
    
    def __init__(self, obj, nb_subdivision) :
        self.sub = nb_subdivision
        bpy.ops.object.mode_set(mode = 'OBJECT')    
        #on va bosser sur une copie de l'obj afin de conserver la cellule de base
        self.base_obj = obj
        self.work_area = self.base_obj.copy()
        self.work_area.data = self.base_obj.data.copy()
        self.work_area.name = 'Grid'
        self.work_area.animation_data_clear()
        bpy.context.scene.objects.link(self.work_area)
        
#obj = bpy.data.objects['Plane_cell.001_cell.017']        
#test = Cell_To_Grid(obj, nb_subdivision=2)        
#test.get_cell_grid_center(test.base_obj)
#test.make_grid()
#res = test.get_angle(Vector((-0.11938, -1.85625, 0.0)))
#res = test.get_angle(Vector((-1.26492, -0.29420, 0.0)))
#res = test.get_angle(Vector((-0.82042, 1.69109, 0.0)))
#res = test.get_angle(Vector((0.76918, 2.16895, 0.0)))
#res = test.get_angle(Vector((1.43554, -1.70960, 0.0)))
#print("base obj area :", test.get_area(test.base_obj))
#print("work area area",test.get_area(test.work_area))
#house = bpy.data.objects['64']      
#house.rotation_euler[2] = res
	
#cell = bpy.data.objects['Plane_cell.001_cell.001']        
#scale_percentage(cell, house, 1)