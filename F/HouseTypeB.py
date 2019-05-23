import bpy
import bmesh
import sys
import os

IMPORTS = ["F\_Utils.py", "WindowGenerator.py", "Door.py", "Materil.py"] 
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

class House :
    
    def set_3d_cursor(self) :
        obj = bpy.data.objects[self.name]
        mesh = bpy.data.meshes[self.obj_name]
        bpy.ops.object.mode_set(mode = 'EDIT')  
        bpy.ops.mesh.select_all(action = 'DESELECT') 
        pos = ( coord_fix(obj, mesh.vertices[18].co) 
            +   coord_fix(obj, mesh.vertices[20].co)
            +   coord_fix(obj, mesh.vertices[22].co))/3 
        previous_context = bpy.context.area.type
        bpy.context.area.type = 'VIEW_3D'
        bpy.context.scene.cursor_location = pos
        bpy.context.area.type = 'TEXT_EDITOR'
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.context.area.type = previous_context
    
    #verif length_front > width_L + 1
    def __init__(self, height, width_front, length_front, width_L, length_L, roof_height, roof_width) :
         #sert a garder une trace des indices de debut et de fin des objets 
        self.width_front = width_front
        self.height = height
        self.length_front = length_front
        self.width_L = width_L
        self.length_L = length_L
        self.roof_height = roof_height
        self.roof_width = roof_width
        self.architecture = {
            'walls'         : (0, -1),
            #ERREUR SUR LES INDICES : LES FACES (14, 9) et (10, 1) peuvent être interchangées -> il faut trouver une nouvelle façon de selectionner les faces du contour des maison !!!!
            'walls_face_id' : [11, 12, 13, 15, 16, 17], 
            'roof'          : (0, -1),
            'porte'         : (0, -1),
            'windows'       : [(0, -1)],
            'decorations'   : [(0, -1)],
            
        }
        walls_ind = self.init_type_b_house()
        self.architecture['walls'] = (0, walls_ind)
      
        
        roof_ind = self.init_roof()
        self.architecture['roof'] = (walls_ind + 1, roof_ind)
        #self.debug_archi()
        self.set_3d_cursor()
        self.init_windows()
        self.init_door()
        
    def init_type_b_house(self) :
        bpy.ops.object.mode_set(mode = 'OBJECT') 
        #Tout commence par un cube
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
        #on calcule l'avancée 
        avancee = self.length_front - self.width_L
         #on scale pour ne plus avoir a le faire plus tard
        bpy.ops.transform.resize(value = (self.width_front, avancee, self.height), constraint_axis=(True, True, True)) 
        bpy.ops.object.mode_set(mode = 'EDIT')
        #on recupere notre mesh que l'on va encore modifier
        bm = bmesh.from_edit_mesh(bpy.context.edit_object.data)
        bm.edges.ensure_lookup_table()
        #on sait que l'arete 6 va bouger
        bm.edges[6].select=True
        bm.edges[6].verts[0].co[1] = bm.edges[6].verts[0].co[1] + self.width_L
        bm.edges[6].verts[1].co[1] = bm.edges[6].verts[1].co[1] + self.width_L
        F_Utils.deselect_All()
        
        bpy.ops.object.editmode_toggle()
        bm = bmesh.from_edit_mesh(bpy.context.edit_object.data)
        bm.faces.ensure_lookup_table()
        bm.faces[1].select = True
         
        print(override) 
        bpy.ops.mesh.extrude_region_move(
            MESH_OT_extrude_region = {
                "mirror":False
            },
            TRANSFORM_OT_translate = { 
                "value":(-self.length_L, 0, 0),
                "constraint_axis":(True, False, False),
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
        bpy.ops.transform.resize(value=(0, 1, 1), constraint_axis=(True, False, False)) 
        #House.deselect_All()
        reset_context()
        #loop cut ici
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
                "edge_index"            : 4,
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
        F_Utils.deselect_All()
        bpy.context.object.active_material_index = 1
        return len(mesh.vertices)
        
    def init_roof(self) :
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_mode(type='VERT')
        bm = bmesh.from_edit_mesh(bpy.context.edit_object.data)
        #on selectionne les faces qui pointent le plus vers le haut (notre toiture)
        for face in bm.faces:
            if face.normal[2] > 0:
                face.select_set(True)  
        bpy.ops.object.material_slot_assign()      
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
        # On va tricher a défaut d'avoir un critère de sélection.
        # y += height o roof ou y -= height o roof (normal)
        # z -= height of roof 
        #Comme notre construction est toujours la même on s'attend à ce que les indices des sommets soient inchangés d'une maison à l'autre.
        bm.verts.ensure_lookup_table()
        y = bm.verts[24].co[1]
        for vert in bm.verts :
            if vert.index == 35 or vert.index == 37 :
                hfix = vert.co[0]
                if hfix == 0 :
                    hfix = 1
                vert.co[0] += (abs(vert.co[0])/hfix) * self.roof_width 
                vert.co[2] -= self.roof_width
            elif vert.index == 36 or vert.index == 38 :
                hfix = vert.co[0]
                if hfix == 0 :
                    hfix = 1   
                vert.co[0] += (abs(vert.co[0])/hfix) * self.roof_width 
                hfix = vert.co[1]
                if y == hfix :
                    hfix =  1
                vert.co[1] -= (abs(y - vert.co[1])/(y - hfix)) * self.roof_width 
                vert.co[2] -= self.roof_width
            elif vert.index == 39 or vert.index == 40 :
                hfix = vert.co[1]
                if hfix == y :
                    hfix =  1
                vert.co[1] -= (abs(y - vert.co[1])/(y - hfix)) * self.roof_width
                vert.co[2] -= self.roof_width    
        
        bpy.ops.object.mode_set(mode = 'EDIT') 
        bm.faces.ensure_lookup_table()
        #selectionner le toit 
        bpy.ops.mesh.select_all(action = 'DESELECT')
        
        select = [f for f in bm.faces if abs(f.normal[0]) == 1 or abs(f.normal[1]) == 1]
        for f in select :
            for v in f.verts :
                if v.index == 42 or v.index == 43 :
                    f.select = True
        bpy.ops.mesh.select_mode(type='FACE')
        bpy.ops.transform.shrink_fatten(value = -self.roof_width * 0.5)         
        return len(bm.verts) 
    
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
  
#height, width_front, length_front, width_L, length_L, house_roof_height, roof_width    
#h = House(1, 3, 4, 2, 6, 4, 0.45)    