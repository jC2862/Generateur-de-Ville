import bpy
import random
import bmesh



def cleanAll():
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

cleanAll()

def createRoad(edges):
    bpy.ops.object.mode_set(mode = 'OBJECT')
    for edge1 in edges :
        width = random.uniform(0.1,0.2)
        print(edge1)
        v0 = edge1.verts[0]
        v1 = edge1.verts[1]
        
        vRoad1 = bm.verts.new((v0.co[0] + width,v0.co[1] + width, v0.co[2] + 0.2))
        vRoad2 = bm.verts.new((v1.co[0] + width,v1.co[1] + width, v0.co[2] + 0.2))
        vRoad3 = bm.verts.new((v1.co[0] - width,v1.co[1] - width, v0.co[2] + 0.2))
        vRoad4 = bm.verts.new((v0.co[0] - width,v0.co[1] - width, v0.co[2] + 0.2))
        
        bm.faces.new([vRoad1, vRoad2, vRoad3, vRoad4])

    # Save et fermeture du bmesh

    bm.to_mesh(me)


bpy.data.screens["Scripting"].name = "Scripting"

#Creation d'un grille de taille 10
bpy.ops.mesh.primitive_grid_add(radius=10, view_align=False, enter_editmode=False, location=(0,0,0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)) 

principalEdges = []


            
bpy.ops.object.mode_set(mode = 'EDIT')

#Application du random 
bpy.ops.transform.vertex_random(offset=0.6,seed=random.randint(0,9999))

#On met tous les Z a 0
bpy.ops.transform.resize(value=(1, 1, 0), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

bpy.ops.object.mode_set(mode = 'OBJECT')
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.transform_apply()
bpy.ops.object.select_all(action='DESELECT')

obj = bpy.context.active_object
me = obj.data
bm = bmesh.new()   
bm.from_mesh(me) 
bm.verts.ensure_lookup_table()
bm.faces.ensure_lookup_table()

for edge in bm.edges :
    #print("edge")
    #for vert in edge.verts :
        #print(vert.co)
    tmpEdge = edge
    principalEdges.append(tmpEdge)

#nbFaces = len(me.polygons)

#Découpage des faces de facon aléatoir 
bpy.ops.object.mode_set(mode = 'EDIT')
bpy.ops.mesh.select_mode(type='FACE')
for i in range(1,3):
    bpy.ops.mesh.select_random(percent = 30,seed=random.randint(0,9999))
    bpy.ops.mesh.subdivide(number_cuts=1, smoothness=0)
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action = 'DESELECT')




#selection des faces 
#TODO meilleur selection pour eviter les problemes 
bpy.ops.mesh.select_random(percent = 50)
bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, random.uniform(0,0.8)), "constraint_axis":(False, False, True), "constraint_orientation":'NORMAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

bpy.ops.object.mode_set(mode = 'OBJECT')
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.transform_apply()
bpy.ops.object.select_all(action='DESELECT')
bm.verts.ensure_lookup_table()
bm.faces.ensure_lookup_table()
bm.from_mesh(me) 
bpy.ops.object.mode_set(mode = 'EDIT')

#stockage des indices des faces selectionnées
index = []
for f in bm.faces:
    if f.select:
        index.append(f.index)
        
bpy.ops.mesh.select_all(action = 'DESELECT')

#parcours des faces precedement selectionnées
for i in index : 
    #print (i)
    
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    
    faceTmp = bm.faces[i]
    if (len(faceTmp.verts) == 5) :
        print(i)
        bm.faces[i].select = True  
        for vert in faceTmp.verts :
            print(vert.co)
    
    #bmesh.update_edit_mesh(me, True)
   
createRoad(principalEdges)
bpy.ops.object.mode_set(mode = 'OBJECT')

bpy.ops.object.camera_add(view_align=True, enter_editmode=False, location=(25, -5, 20), rotation=(0.842695, 0.0112104, 1.40433), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
bpy.ops.object.lamp_add(type='POINT', radius=1, view_align=False, location=(0, -10.2429, 8.6231), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))

