import bpy
import bmesh
from math import sqrt, atan2, acos
from mathutils import Vector
from numpy import dot, cross

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

#@ deprecated 
def mend_face(face) :
    #face impaire
    if len(face.verts) % 2 == 0 : return

    longest = face.edges[0]   
    # on récupère la plus longue arete 
    for edge in face.edges :
        print("edge i : {} \ length : {}".format(edge.index, dist_fix(edge)))
        if dist_fix(edge) > dist_fix(longest) :
            longest = edge
    #on divise cette arete en deux     
    longest.select = True   
    bpy.ops.mesh.subdivide(smoothness = 0)
    
def sortDist(edge) :
    return dist_fix(edge)

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

def norm(u) : 
    return sqrt(u[0] ** 2 + u[1] ** 2 + u[2] ** 2) 

#le cos devrait suffire !!!!!
def angle_between(u, v) :
    n_u = norm(u)
    n_v = norm(v)
    x = dot(u, v) / (n_u * n_v)
    print("cos alpha : ", x)
    vec_tmp = cross(v, u)
    n_tmp = norm(vec_tmp)
    return atan2(dot(cross(u, v), vec_tmp), x)    

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
    

def calc_rotation(object, border) :
    #test = Vector(center[0], center[1] - 1, center[2])
    # de la forme : (face index, [edges index])
    bpy.ops.object.mode_set(mode = 'EDIT')
    vec = Vector((0, 1, 0))
    list = []
    for elt in border : 
        center_face = get_center_median(object, elt[0])
        center_edge = get_center_edge(object, elt[1])
        #print(center_edge)
        target = Vector(center_edge) - Vector(center_face)
        #vec = Vector(center_face) - Vector((0, -1, 0))
        print("face N°{} : target  {}".format(elt[0], target))
        list.append((elt[0], angle_between(target, vec)))
    #
    #target = Vector((0, 0, 0))
    return list 
    
def move_and_rotate(obj_name, dest, rot) :
    save = bpy.context.scene.objects.active 
    bpy.ops.mesh.select_all(action='DESELECT')   
    obj = bpy.data.objects[obj_name] 
    bpy.context.scene.objects.active = obj
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.context.scene.objects.active.location = dest
    bpy.context.scene.objects.active.rotation_euler = (0, 0, rot)
    bpy.context.scene.objects.active = save
    #bpy.ops.transform.rotate(value=rot, axis=(0, 0, 1), constraint_axis=(False, False, True))
  
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
    return area  
   
def scale_percentage(cell, object, face) :
    bpy.ops.object.mode_set(mode = 'EDIT')
    bound_area = get_bounding_box_area(object.name)
    
    bpy.context.scene.objects.active = cell
    bpy.ops.object.mode_set(mode = 'EDIT')
    bm = bmesh.from_edit_mesh(cell.data) 
    
    bm.faces.ensure_lookup_table()
    face_area = bm.faces[face].calc_area()
    scale = 1/((bound_area / face_area))
    #print("SCALEEEEEEEEEEEE : ", scale)

    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.scene.objects.active = object
    object.scale[0] = scale * 10
    object.scale[1] = scale * 10
    object.scale[2] = scale * 10
    
def fix_face(obj_cell) :
    #travaillons sur duplica de la cellule ? <- peut-etre pas necessaire !!!
    bpy.context.scene.objects.active = obj_cell
    if bpy.context.mode != 'EDIT' :
        bpy.ops.object.mode_set(mode = 'EDIT')
    bm = bmesh.from_edit_mesh(obj_cell.data)
        
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
            obj_cell.data.edges[elt].select = True
        
        bpy.ops.object.mode_set(mode = 'EDIT')     
        bpy.ops.mesh.merge(type='COLLAPSE')
        
        bm = bmesh.from_edit_mesh(obj_cell.data)
        bm.faces.ensure_lookup_table()
        #center = get_center_median(name, 0)
        #print(center)
    
    bpy.ops.mesh.select_all(action='SELECT')    
    bpy.ops.mesh.subdivide(number_cuts = 3)
    
    bpy.ops.mesh.region_to_loop()
    #on va enregistrer les indices des aretes du bord de la cellule.
    
    #puis calculer la rotation
    
#bm = bmesh.from_edit_mesh(bpy.context.active_object.data)
#obj = bpy.context.active_object.data
#fix_face(obj) 
#res = select_boundary_face(obj)
#list = calc_rotation(res)
#print(list)

#on passe en global parce que c est cool le global
#center_face = coord_fix(get_center_median(list[0][0]))
#house = bpy.data.objects['House']
#move_and_rotate(house, center_face, list[0][1])
#scale_percentage('House', 0)