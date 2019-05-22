import random as R
import Utils as U
import bmesh
import bpy
from mathutils import Vector

visited_node = [] 

def recur(center, node, level):
    if(level < 1 or (node in visited_node)):return None
    visited_node.append(node)
    next = []
    for face in node.link_faces:
        for v in face.verts:
            if abs(v.co.z-center.co.z) < 0.1:
                E = recur(center, v, level-1)
                if E != None:
                    if(type(E) != bmesh.types.BMVert):
                        for e in E:
                            next.append(e)
                    else:
                        next.append(E)
    return next if len(next) > 0 else node



def min_vert(verts):
    min_ver = verts[0]
    min_val = min_ver.co.z

    for v in verts:
        if(v.co.z < min_val):
            min_val = v.co.z
            min_ver = v

    return min_ver



def findPlaceIn(terrain):

    U.unselect()
    U.select(terrain)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    
    bm = bmesh.from_edit_mesh(terrain.data)
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()

    Center = min_vert(bm.verts)
    
    #bm.verts[R.randint(0,len(bm.verts))]
    print("FACES")
    visited_node.append(Center)
    arg = []
    for face in Center.link_faces:
        print(face)
        for v in face.verts:
            E = recur(Center, v, 150)
            #print(E)
            if E != None:
                print("AZE " + str(E))
                arg = E
    bpy.ops.mesh.select_all(action='DESELECT')
    '''
    for v in visited_node:
        v.select = True
    '''
    vec =  terrain.matrix_world * Center.co 
    bpy.ops.object.mode_set(mode='OBJECT')
    return vec



    