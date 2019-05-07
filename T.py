import bpy
import bmesh
import random
import mathutils

def cleanAll():
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def updateMesh(me):
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.transform_apply()
    bpy.ops.object.select_all(action='DESELECT')
    bm.from_mesh(me) 

def max (a,b,c,d) :
    max = a
    if b > max :
        max = b
    elif c > max :
        max = c
    elif d > max :
        max = d
    return max

def min (a,b,c,d) :
    min = a
    if b < min :
        min = b
    elif c < min :
        min = c
    elif d < min :
        min = d
    return min

def percent (max, current) :
	percent = (current/max)*100
	print(int(percent) , "%")

def setColorAll(obj, color):
    bpy.ops.object.mode_set(mode = 'OBJECT')
    if color not in obj.data.materials:
        obj.data.materials.append(bpy.data.materials[color])
    indexMat = obj.data.materials.find(color)
    for p in obj.data.polygons:
        obj.data.polygons[p.index].material_index = indexMat

def cuboidV2(v1,v2,nbCuboid,width):
	
	direct = v1.co - v2.co
	len = direct.length
	mesh_data2 = bpy.data.meshes.new("Cobble")
	for i in range(0,nbCuboid) :
	    CobbleSize = random.uniform(width/8,width/4) #taille du pavé
	    fact = random.uniform(0,1) #permet de placer le pavé sur l'axe principal de la route
	    decalage = random.uniform(-width/1.5,width/1.5) #décalage du pavé par rapport a l'axe principal
	    height = CobbleSize/2 #hauteur du pavé
	    XCobble = v1.co[0] - direct[0]*fact #Coordonnées du pavé
	    YCobble = v1.co[1] - direct[1]*fact
	    
	    #face supperieur du pavé
	    VCobble1 = bm.verts.new((	XCobble+decalage,
	    							YCobble+decalage,
	    							v1.co[2]+0.2 + height))
	    VCobble2 = bm.verts.new((	XCobble+CobbleSize+decalage,
	    							YCobble+decalage,
	    							v1.co[2]+0.2+ height))
	    VCobble3 = bm.verts.new((	XCobble+CobbleSize+decalage,
	    							YCobble+CobbleSize+decalage,
	    							v1.co[2]+0.2+ height))
	    VCobble4 = bm.verts.new((	XCobble+decalage,
	    							YCobble+CobbleSize+decalage,
	    							v1.co[2]+0.2+ height))
	    
	    #face inferieur du pavé
	    BotVCobble1 = bm.verts.new((VCobble1.co[0],VCobble1.co[1],v1.co[2]+0.2))
	    BotVCobble2 = bm.verts.new((VCobble2.co[0],VCobble2.co[1],v1.co[2]+0.2))
	    BotVCobble3 = bm.verts.new((VCobble3.co[0],VCobble3.co[1],v1.co[2]+0.2))
	    BotVCobble4 = bm.verts.new((VCobble4.co[0],VCobble4.co[1],v1.co[2]+0.2))
	    
	    #top face
	    bm.faces.new([VCobble1, VCobble2, VCobble3, VCobble4])        
	    #lateral faces
	    bm.faces.new([VCobble1, VCobble2, BotVCobble2, BotVCobble1])  
	    bm.faces.new([VCobble2, VCobble3, BotVCobble3, BotVCobble2])  
	    bm.faces.new([VCobble3, VCobble4, BotVCobble4, BotVCobble3])  
	    bm.faces.new([VCobble4, VCobble1, BotVCobble1, BotVCobble4])
	    
	obj = bpy.data.objects.new("Cobble", mesh_data2)
	newColor((0.3,0.2,0.2),"CobbleCol")
	Cobble = bpy.context.scene.objects[1]
	setColorAll(Cobble, "CobbleCol")
	bm.to_mesh(me)

def newColor(col, name):
    mat = bpy.data.materials.get(name)
    if mat == None:
        mat = bpy.data.materials.new(name)
    mat.diffuse_color = col
    
def createRoad (edge) :

    mesh_data = bpy.data.meshes.new("road")
    bpy.ops.object.mode_set(mode = 'OBJECT')

    #print(edge)
    v0 = edge.verts[0]
    v1 = edge.verts[1]
    
    direct = v0.co - v1.co
    len = direct.length
    #print("len" , len)
    direct = direct.normalized()
    direct.resize_2d()
    ortho = direct.orthogonal()
    #print(ortho)
    

    width = random.uniform(len/20,len*2/20)
    pavement = random.uniform(width/10,width/5)

    vRoad1 = bm.verts.new(( v0.co[0] + ortho.x*width,   #x
                            v0.co[1] + ortho.y*width,   #y
                            v0.co[2] + 0.2))            #z
    vRoad2 = bm.verts.new(( v1.co[0] + ortho.x*width,   
                            v1.co[1] + ortho.y*width, 
                            v0.co[2] + 0.2))
    vRoad3 = bm.verts.new(( v1.co[0] - ortho.x*width,
                            v1.co[1] - ortho.y*width, 
                            v0.co[2] + 0.2))
    vRoad4 = bm.verts.new(( v0.co[0] - ortho.x*width,
                            v0.co[1] - ortho.y*width, 
                            v0.co[2] + 0.2))
    
    #upper pavement face
    vRoad5 = bm.verts.new(( v0.co[0] + ortho.x*width + pavement - direct[0]*width*1.5,
                            v0.co[1] + ortho.y*width + pavement - direct[1]*width*1.5,
                            v0.co[2] + 0.25))
    vRoad6 = bm.verts.new(( v1.co[0] + ortho.x*width + pavement + direct[0]*width*1.5,
                            v1.co[1] + ortho.y*width + pavement + direct[1]*width*1.5, 
                            v0.co[2] + 0.25))
    vRoad7 = bm.verts.new(( v1.co[0] + ortho.x*width + direct[0]*width*1.5,
                            v1.co[1] + ortho.y*width + direct[1]*width*1.5, 
                            v0.co[2] + 0.25))
    vRoad8 = bm.verts.new(( v0.co[0] + ortho.x*width - direct[0]*width*1.5,
                            v0.co[1] + ortho.y*width - direct[1]*width*1.5, 
                            v0.co[2] + 0.25)) 
       
    #upper pavement face
    vRoad9 = bm.verts.new(( v0.co[0] - ortho.x*width - direct[0]*width*1.5,
                            v0.co[1] - ortho.y*width - direct[1]*width*1.5, 
                            v0.co[2] + 0.25))
    vRoad10 = bm.verts.new((v1.co[0] - ortho.x*width + direct[0]*width*1.5,
                            v1.co[1] - ortho.y*width + direct[1]*width*1.5, 
                            v0.co[2] + 0.25))
    vRoad11 = bm.verts.new((v1.co[0] - ortho.x*width - pavement + direct[0]*width*1.5,
                            v1.co[1] - ortho.y*width - pavement + direct[1]*width*1.5, 
                            v0.co[2] + 0.25))
    vRoad12 = bm.verts.new((v0.co[0] - ortho.x*width - pavement - direct[0]*width*1.5,
                            v0.co[1] - ortho.y*width - pavement - direct[1]*width*1.5, 
                            v0.co[2] + 0.25))
    
    #side pav face
    vRoad5low = bm.verts.new((  v0.co[0] + ortho.x*width + pavement - direct[0]*width,
                                v0.co[1] + ortho.y*width + pavement - direct[1]*width, 
                                v0.co[2]+ 0.2))
    vRoad6low = bm.verts.new((  v1.co[0] + ortho.x*width + pavement + direct[0]*width,
                                v1.co[1] + ortho.y*width + pavement + direct[1]*width, 
                                v0.co[2]+ 0.2))
    vRoad7low = bm.verts.new((  v1.co[0] + ortho.x*width + direct[0]*width,
                                v1.co[1] + ortho.y*width + direct[1]*width, 
                                v0.co[2]+ 0.2))
    vRoad8low = bm.verts.new((  v0.co[0] + ortho.x*width - direct[0]*width,
                                v0.co[1] + ortho.y*width - direct[1]*width, 
                                v0.co[2]+ 0.2)) 
    
    
    #side pav face
    vRoad9low = bm.verts.new(( v0.co[0] - ortho.x*width - direct[0]*width,
                            v0.co[1] - ortho.y*width - direct[1]*width, 
                            v0.co[2] + 0.20))
    vRoad10low = bm.verts.new((v1.co[0] - ortho.x*width + direct[0]*width,
                            v1.co[1] - ortho.y*width + direct[1]*width, 
                            v0.co[2] + 0.20))
    vRoad11low = bm.verts.new((v1.co[0] - ortho.x*width - pavement + direct[0]*width,
                            v1.co[1] - ortho.y*width - pavement + direct[1]*width, 
                            v0.co[2] + 0.20))
    vRoad12low = bm.verts.new((v0.co[0] - ortho.x*width - pavement - direct[0]*width,
                            v0.co[1] - ortho.y*width - pavement - direct[1]*width, 
                            v0.co[2] + 0.20))
    
    
    cuboidV2(v0,v1,random.randint(int(len*2),int(len*4)),width)
    bm.faces.new([vRoad1, vRoad2, vRoad3, vRoad4])
    
    #pavement
    if len > 1:
        
        bm.faces.new([vRoad5, vRoad6, vRoad7, vRoad8])
        bm.faces.new([vRoad9, vRoad10, vRoad11, vRoad12])
        bm.faces.new([vRoad8low, vRoad7low, vRoad7, vRoad8])
        bm.faces.new([vRoad10low, vRoad9low, vRoad9, vRoad10])
        
        bm.faces.new([vRoad5, vRoad6, vRoad6low, vRoad5low])
        bm.faces.new([vRoad11, vRoad12, vRoad12low, vRoad11low])
        
        bm.faces.new([vRoad6, vRoad7, vRoad7low, vRoad6low])
        bm.faces.new([vRoad5, vRoad8, vRoad8low, vRoad5low])
        bm.faces.new([vRoad10, vRoad11, vRoad11low, vRoad10low])
        bm.faces.new([vRoad9, vRoad12, vRoad12low, vRoad9low])
    # Save et fermeture du bmesh
    
    obj = bpy.data.objects.new("My_Object", mesh_data)
    newColor((0.5,0.4,0.4),"roadCol")
    monObj = bpy.context.scene.objects[0]
    setColorAll(monObj, "roadCol")
    
    
    
import J
import time

cleanAll()
start2 = time.time()
J.execute()

for CurObj in bpy.context.scene.objects :
	CurObj.select = True
	bpy.context.scene.objects.active = CurObj
	me = bpy.context.object.data
	bpy.ops.object.mode_set(mode = 'EDIT')

	bpy.ops.mesh.delete(type='ONLY_FACE')
	bpy.ops.mesh.select_mode(type = 'EDGE')
	bpy.ops.mesh.select_all(action='SELECT')
	bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0,0,0)})
	bpy.ops.transform.resize(value=(0.9, 0.9, 0.9))

	bpy.ops.mesh.select_mode(type = 'FACE')
	bpy.ops.mesh.select_all(action='SELECT')
	bpy.ops.mesh.extrude_region_move(
		TRANSFORM_OT_translate={"value":(0, 0, 0.05) })

	bpy.ops.object.mode_set(mode='OBJECT')

# 	bpy.ops.mesh.inset(
# 		use_boundary=True, 
# 		thickness=0.2,
# 		use_even_offset = True)
# 	bpy.ops.mesh.select_all(action='INVERT')
# 	# bpy.ops.mesh.select_face_by_sides()
# 	bpy.ops.object.mode_set(mode = 'OBJECT')
# 	CurObj.select = False

# bpy.ops.mesh.primitive_plane_add(radius=10,location=(0, 0, -0.001))




























	#CurObj.select = False
# end2 = time.time()
# start = time.time()

# C = bpy.context
# scene = C.scene
# bpy.data.objects['Test'].select=True
# scene.objects.active = bpy.data.objects['Test']
# #bpy.ops.mesh.primitive_grid_add(radius=10, view_align=False, enter_editmode=False, location=(0,0,0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))

# me = bpy.context.object.data

# bm = bmesh.new()   
# bm.from_mesh(me)   



# nbEdges = len(bm.edges) 
# print(nbEdges)
# for index in range(0,nbEdges) :
#     bm.verts.ensure_lookup_table()
#     bm.faces.ensure_lookup_table()
#     bm.edges.ensure_lookup_table()
#     #print(index)
#     createRoad(bm.edges[index])
#     percent(nbEdges,index)
# bm.to_mesh(me)
# bm.free()
# #print()
# end = time.time()
# print("nombre edges : ", nbEdges)
# print("time LSystem: ",end2 - start2)
# print("time route: ",end - start)
# bpy.ops.object.editmode_toggle()
# bpy.ops.mesh.delete(type='VERT')
# bpy.ops.object.editmode_toggle()