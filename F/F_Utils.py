import bpy
import bmesh

#Utile pour faire un loop cut / deplacer le curseur3D
def view3d_find( return_area = False ):
    # returns first 3d view, normally we get from context
    for area in bpy.context.window.screen.areas:
        if area.type == 'VIEW_3D':
            v3d = area.spaces[0]
            rv3d = v3d.region_3d
            for region in area.regions:
                if region.type == 'WINDOW':
                    if return_area: return region, rv3d, v3d, area
                    return region, rv3d, v3d
    return None, None

region, rv3d, v3d, area = view3d_find(True)

override = {
    'scene'  : bpy.context.scene,
    'region' : region,
    'area'   : area,
    'space'  : v3d
}

def deselect_All() :
    #deselect everything
    bpy.context.object.update_from_editmode() # Loads edit-mode data into object data
    bpy.ops.object.mode_set(mode = 'EDIT') 
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT') 
    
def clean_All() : 
    # Supprime tous les éléments de la scène
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)   
    
def clean_Current() :
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode = 'EDIT') 
    bpy.data.objects.remove(bpy.context.edit_object.data, True)      
    bpy.ops.object.mode_set(mode = 'OBJECT') 
    
#coord globales
def coord_fix(vertex) :
    obj = bpy.context.active_object
    return obj.matrix_world * vertex

def dist_fix(edge) :
    pt0 = coord_fix(edge.verts[0].co)
    pt1 = coord_fix(edge.verts[1].co)    
    return sqrt( (pt1[0] - pt0[0]) ** 2
                +(pt1[1] - pt0[1]) ** 2
                +(pt1[2] - pt0[2]) ** 2
                )        