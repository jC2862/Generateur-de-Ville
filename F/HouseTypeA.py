import bpy
import bmesh
import sys
import os
from math import sqrt

IMPORTS = ["F\_Utils.py", "WindowGenerator.py", "Door.py" "Material.py"] 
dir_path = os.path.dirname(os.path.realpath(__file__))
for im in IMPORTS:
    print(dir_path+"/"+im)
    sys.path.append(dir_path+"/"+im)
import F_Utils, WindowGenerator, Door, Material

region, rv3d, v3d, area = F_Utils.view3d_find(True)

override = {
    'scene'  : bpy.context.scene,
    'region' : region,
    'area'   : area,
    'space'  : v3d
}

def reset_context() :
    region, rv3d, v3d, area = F_Utils.view3d_find(True)

    override = {
        'scene'  : bpy.context.scene,
        'region' : region,
        'area'   : area,
        'space'  : v3d
    }

def coord_fix(obj, vertex) :
    return obj.matrix_world * vertex
##########################################################################


class House:
    
    def set_3d_cursor(self) :
        obj = bpy.data.objects[self.name]
        mesh = bpy.data.meshes[self.obj_name]
        bpy.ops.object.mode_set(mode = 'EDIT')  
        bpy.ops.mesh.select_all(action = 'DESELECT') 
        print(coord_fix(obj, mesh.vertices[12].co)) 
        pos = (coord_fix(obj, mesh.vertices[12].co) 
            + coord_fix(obj, mesh.vertices[14].co))/2  
        previous_context = bpy.context.area.type
        bpy.context.area.type = 'VIEW_3D'
        bpy.context.scene.cursor_location = pos
        bpy.context.area.type = 'TEXT_EDITOR'
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.context.area.type = previous_context
    
    def __init__(self, height, width, length, roof_height, roof_width) :
        #sert a garder une trace des indices de debut et de fin des objets 
        self.width = width
        self.height = height
        self.length = length
        self.roof_height = roof_height
        self.roof_width = roof_width
        self.architecture = {
            'walls'         : (0, -1),
            #on connait d'avance les indices des faces qui forment les murs (par construction)
            'walls_face_id' : [6, 7, 8, 9, 10, 11],
            'roof'          : (0, -1),
            'porte'         : (0, -1),
            'windows'       : [(0, -1)],
            'decorations'   : [(0, -1)],
            
        }
        walls_ind = self.init_house()
        self.architecture['walls'] = (0, walls_ind)
        F_Utils.deselect_All()
        
        roof_ind = self.init_roof()
        self.architecture['roof'] = (walls_ind + 1, roof_ind)
        self.debug_archi()
        self.set_3d_cursor()
        self.init_windows()
        self.init_door()
        
    def debug_archi(self) :
        for k, v in self.architecture.items() :
            print("{} : {}".format(k, v))    
    
    def init_house(self) :
        #on ajoute un cube ...
        bpy.ops.object.mode_set(mode = 'OBJECT')  
        bpy.ops.mesh.primitive_cube_add()
        bpy.context.object.data.name = 'House'
        bpy.context.object.name = 'House'
        #on sauvegarde le nom de la maison pour identifier le mesh qui lui correspond !
        self.obj_name = bpy.context.object.data.name
        self.name = bpy.context.object.name
        
        obj = bpy.context.scene.objects.active
        Material.affect_mat(obj, self.name + "_Wall_mat", 'Wall')
        Material.affect_mat(obj, self.name + "_Roof_mat", 'Roof')
        bpy.context.object.active_material_index = 0
        #...que l'on va modifier
        bpy.ops.object.editmode_toggle()
        #on scale pour donner une largeur, longeur et hauteur a notre maison
        bpy.ops.transform.resize(value = (self.width, self.length, self.height), constraint_axis=(True, True, True))  
        reset_context()
        #on fait une loop cut automatiquement afin de séparer la maison en 2
        bpy.ops.mesh.loopcut_slide(
            override, 
            MESH_OT_loopcut = {
                "number_cuts"           : 1,
                "smoothness"            : 0,     
                "falloff"               : 'INVERSE_SQUARE',
                "edge_index"            : 3,
                "mesh_select_mode_init" : (False, True, False)
            },
            TRANSFORM_OT_edge_slide = {
                "value"           : -0.85,
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
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.mesh.loopcut_slide(
            override, 
            MESH_OT_loopcut = {
                "number_cuts"           : 1,
                "smoothness"            : 0,     
                "falloff"               : 'INVERSE_SQUARE',
                "edge_index"            : 11,
                "mesh_select_mode_init" : (False, True, False)
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
        #a l issue du loop cut, 4 sommets sont selectionnes
        bpy.ops.object.mode_set(mode = 'OBJECT') 
        mesh = bpy.context.object.data
        bpy.context.object.update_from_editmode() # Loads edit-mode data into object data
        #on va deselectionner les 2 sommets du dessous du mesh et tirer vers le haut les deux autres
        for vert in mesh.vertices :
            if vert.select and vert.co[2] != self.height :
                vert.select = False
        #on doit aussi deselectionner les aretes correspondantes
        for edge in mesh.edges :
            a = edge.vertices[0]
            b = edge.vertices[1]       
            if not mesh.vertices[a].select or not mesh.vertices[b].select :
                edge.select = False 
                
        bpy.ops.object.mode_set(mode = 'EDIT') 
        #on rehausse nos deux points 
        bpy.ops.transform.translate(value = (0, 0, self.roof_height), constraint_axis=(False, False, True), constraint_orientation='GLOBAL')       
        bpy.context.object.update_from_editmode() # Loads edit-mode data into object data
        bpy.ops.object.mode_set(mode = 'EDIT')
        #par construction, les sommets 12 et 14 sont les sommets du bas de la maison, on fait du centre median de ces sommets le centre de l'objet
        bpy.context.object.active_material_index = 1          
        return len(mesh.vertices)
    
    def init_roof(self) :
        bpy.ops.object.mode_set(mode = 'EDIT') 
        bm = bmesh.from_edit_mesh(bpy.context.edit_object.data)
        #on selectionne les faces qui pointent le plus vers le haut (notre toiture)
        for face in bm.faces:
            if face.normal[2] > 0 :
                face.select_set(True)         
        bpy.ops.mesh.duplicate_move()
        bpy.ops.mesh.extrude_region_move(
            MESH_OT_extrude_region = {
                "mirror":False
            },
            TRANSFORM_OT_translate = { 
                "value":(0, 0, self.roof_width),
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
        bpy.ops.mesh.select_all(action = 'DESELECT')
        #1.| faire en sorte que les bords aient la meme hauteur
        # x += height o roof ou x -= height o roof (normal)
        # z -= height of roof 
        bm = bmesh.from_edit_mesh(bpy.context.edit_object.data)
        bm.verts.ensure_lookup_table()
        selected = []
        for ind in range(self.architecture['walls'][1], len(bm.verts)) : 
            print(bm.verts[ind])
            if bm.verts[ind].co[2] == self.height + self.roof_width :
                bm.verts[ind].select = True
                selected.append(ind)
        for ind in selected :
            hotfix = bm.verts[ind].co[0]
            if hotfix == 0  :
                hotfix = 1
            #au pire si hotfix n'est pas bon le résultat sera 0    
            bm.verts[ind].co[0] += (abs(bm.verts[ind].co[0])/hotfix) * self.roof_width 
            bm.verts[ind].co[2] -= self.roof_width
        #choisir le sous-mesh qui fait office de toit 
        #2.| scaler sur l'axe y
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.mesh.select_linked_pick(deselect=False, delimit=set(), index = self.architecture['walls'][1] + 1)
        bpy.ops.object.material_slot_assign()
        #on scale pour creer une avancee a notre toiture
        bpy.ops.transform.resize(value = (0, 1.1, 0), constraint_axis=(False, True, False))
                      
        return len(bm.verts)
    
    def init_door(self) :
        self.door = Door.DoorGenerator(self, self.available)
        
        bpy.ops.object.mode_set(mode = 'OBJECT')  
        
        bpy.context.scene.objects.active = bpy.data.objects[self.name]
        bpy.ops.object.select_all(action='DESELECT') 
        for obj in bpy.context.scene.objects : 
            if obj.name.startswith(self.name + '_') :
                obj.select = True
        bpy.context.scene.objects.active.select = True      
        bpy.ops.object.join()        
        return 0
    
    def init_windows(self) :
        self.available = self.architecture['walls_face_id']
        self.windows = WindowGenerator.WindowGenerator(self, self.available)
        self.available = self.windows.free_walls
        bpy.ops.object.mode_set(mode = 'OBJECT')  
        
        bpy.context.scene.objects.active = bpy.data.objects[self.name]
        bpy.ops.object.select_all(action='DESELECT') 
        for obj in bpy.context.scene.objects : 
            if obj.name.startswith(self.name + '_') :
                obj.select = True
        bpy.context.scene.objects.active.select = True      
        bpy.ops.object.join()        
        return 0
    
##########################################################################                 

#house = House(3,2,3,2,.5)