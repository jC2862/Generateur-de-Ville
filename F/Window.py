import bpy
import bmesh
import os
import sys
from random import uniform
from math import sqrt
from numpy import dot, cross, array, matrix, identity
from numpy.linalg import inv

IMPORTS = ["FaceDrawableArea.py", "F_Utils.py"] 
dir_path = os.path.dirname(os.path.realpath(__file__))
for im in IMPORTS:
    print(dir_path+"/"+im)
    sys.path.append(dir_path+"/"+im)
import FaceDrawableArea, F_Utils

region, rv3d, v3d, area = F_Utils.view3d_find(True)

override = {
    'scene'  : bpy.context.scene,
    'region' : region,
    'area'   : area,
    'space'  : v3d
}

class Window :
    
    #ici la face n'appartient pas vraiment au mesh 'house', c'est une face que l on aura créé à partir           d'une autre
    def __init__(self, house, face, width, height, thickness) :
        self.house = house
        self.face = face
        self.width = width
        self.height = height
        self.thickness = thickness        
        
    def draw_basic(self, rotation) :
        #On dessine directment au bon endroit !!!!
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.mesh.primitive_cube_add()
        bpy.context.object.data.name = self.house.obj_name + '_Window'
        bpy.context.object.name = self.house.name + '_Window'
        #on sauvegarde le nom de la maison pour identifier le mesh qui lui correspond !
        self.obj_name = bpy.context.object.data.name
        self.name = bpy.context.object.name
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.transform.resize(value = (self.width, self.thickness, self.height), constraint_axis = (True, True, True))
        bm = bmesh.from_edit_mesh(bpy.context.active_object.data)

        bm.faces.ensure_lookup_table()
        
        bmesh.ops.inset_region(bm, faces = [bm.faces[3], bm.faces[1]], thickness = self.thickness/2, depth = 0)
        
        #on supprime les faces 1 et 3
        bm.faces.ensure_lookup_table()
        bm.faces.remove(bm.faces[3])
        
        bm.faces.ensure_lookup_table()
        bm.faces.remove(bm.faces[1])
        
        bm.verts.ensure_lookup_table()
        bm.edges.ensure_lookup_table()    
        #on choisit les verts des deux edges loops que l'on va bridge
        loop_1 = [bm.edges[12], bm.edges[17], bm.edges[18], bm.edges[19]]
        loop_2 = [bm.edges[13], bm.edges[14], bm.edges[15], bm.edges[16]]
        
        bmesh.ops.bridge_loops(bm, edges = loop_1+loop_2)
        #bpy.ops.mesh.bridge_edge_loops()
        bpy.ops.mesh.select_all(action = 'DESELECT')
        
        for v in loop_2 : 
            print(v.index)
            v.select = True
        bpy.ops.mesh.edge_face_add()
        
        bpy.ops.mesh.loopcut_slide(
            override, 
            MESH_OT_loopcut = {
                "number_cuts"           : 1,
                "smoothness"            : 0,     
                "falloff"               : 'SMOOTH',
                "edge_index"            : 30,
                "mesh_select_mode_init" : (True, False, False)
            },
            TRANSFORM_OT_edge_slide = {
                "value"           : 0,
                "mirror"          : False, 
                "snap"            : False,
                "snap_target"     : 'CLOSEST',
                "snap_point"      : (0, 0, 0),
                "snap_align"      : False,
                "snap_normal"     : (0, 0, 0),
                "correct_uv"      : False,
                "release_confirm" : False
            }
        )    
        bpy.ops.mesh.edge_face_add()
        bpy.ops.mesh.select_all(action = 'DESELECT')
        #barreau de fenetre vertical
        bpy.ops.mesh.primitive_cube_add()
        bpy.ops.transform.resize(value = (self.thickness * .25, self.thickness * .25, self.height), constraint_axis = (True, True, True))
        #45 degrees = 0.785398 rad 
        bpy.ops.transform.rotate(value = 0.785398, axis = (0, 0, 1), constraint_axis = (False, False, True))
        #barreau de fenetre horizontal
        bpy.ops.mesh.primitive_cube_add()
        bpy.ops.transform.resize(value = (self.width, self.thickness * .25, self.thickness * 0.25), constraint_axis = (True, True, True))
        #45 degrees = 0.785398 rad 
        bpy.ops.transform.rotate(value = 0.785398, axis = (1, 0, 0), constraint_axis = (True, False, False)) 
        bpy.ops.mesh.select_all(action = 'SELECT')
        bpy.ops.transform.rotate(value=rotation, axis=(0,0,1), constraint_axis=(False, False, True))
        bpy.ops.mesh.normals_make_consistent(inside=False)
        

    
    def draw(self, pos = (0, 0, 0), normal = (0, 0, 1), thickness = 0.15, width = .5, height = 1.2) :
        bpy.ops.object.mode_set(mode='OBJECT')
        #on ajoute un plan
        bpy.ops.mesh.primitive_plane_add(location = pos)
        #on scale pour donner une largeur, longeur et hauteur a notre maison
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.transform.resize(value = (width, height, 0), constraint_axis=(True, True, False)) 
        bpy.ops.mesh.inset(thickness = thickness) 
        bpy.ops.mesh.select_mode(use_extend = False, use_expand = False, type = 'FACE')
        bpy.ops.mesh.select_all(action = 'INVERT')
        bpy.ops.mesh.extrude_region_move( MESH_OT_extrude_region = {
                "mirror":False
            },
            TRANSFORM_OT_translate = { 
                "value":(0, 0, thickness),
                "constraint_axis":(False, False, True),
                "constraint_orientation":'GLOBAL',
                "mirror":False, "proportional":'DISABLED',
                "proportional_edit_falloff":'SMOOTH',
                "proportional_size":1, "snap":False,
                "snap_target":'CLOSEST',
                "snap_point":(0, 0, 0),
                "snap_align":False,
                "snap_normal":(0, 0, 0),
                "gpencil_strokes":False,
                "texture_space":False,
                "remove_on_cancel":False, 
                "release_confirm":False,
                "use_accurate":False
            }
        )
        
    def drawTypeB() :
        self.house.modifier_add(type='BOOLEAN')
        self.face.select = True
        #risque de devoir override ou autre !!!
        bpy.ops.view3d.snap_cursor_to_selected()
        #on va creer un creux dans la maison a l'aide du modificateur booleen
        bpy.ops.object.mode_set(mode = 'OBJECT')
        #on ajoute un cube a la position du curseur 3d ie : pas besoin d'idinquer la position
        bpy.ops.mesh.primitive_cube_add()
        #resize sur x, y et z
        bpy.ops.transform.resize()
                 
        #pour cela il nous faut un cube que l'on va scale puis appliquer le modificateur
        #les faces internes creees restent selectionnees.
        #on deselectionne la face du fond
        #on ajoute un loop cut
        #on fill pour créer une vitre
        #on y attribut son material
         #enfin on va supprimer le cube modif ou en faire des volets.