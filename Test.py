import bpy
import math 
import random
import os

dir_path = os.path.dirname(__file__)

#Ajoute une couleur "color" a l'objet "obj"
def setColorAll(obj, color):
    bpy.ops.object.mode_set(mode = 'OBJECT')
    if color not in obj.data.materials:
        obj.data.materials.append(bpy.data.materials[color])
    indexMat = obj.data.materials.find(color)
    for p in obj.data.polygons:
        obj.data.polygons[p.index].material_index = indexMat

#Création d'un nouvelle couleur "col" avec le nom "name"
def newColor(col, name):
    mat = bpy.data.materials.get(name)
    if mat == None:
        mat = bpy.data.materials.new(name)
    mat.diffuse_color = col

def cleanAll():
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for bpy_data_iter in (bpy.data.objects,bpy.data.meshes,bpy.data.lamps,bpy.data.cameras,bpy.data.particles,bpy.data.materials):
        for id_data in bpy_data_iter:
            bpy_data_iter.remove(id_data)

def CreateLog(x,y,z,radius) :
	# bpy.ops.object.select_all(action='DESELECT')
	bpy.ops.mesh.primitive_cylinder_add(
		vertices=8, 
		radius=radius, 
		depth=7*radius, 
		location=(x, y, z), 
		)
	bpy.ops.transform.rotate(
		value= math.pi/2, 
		axis=(0, 1, 0)
		)

	bpy.ops.object.mode_set(mode = 'EDIT')

	bpy.ops.mesh.select_all(action='DESELECT')

	bpy.ops.mesh.select_face_by_sides(number=8, type='EQUAL')
	bpy.ops.mesh.inset(thickness=0.2*radius, depth=0)
	bpy.ops.view3d.snap_cursor_to_center()
	bpy.ops.mesh.extrude_region_shrink_fatten(
		MESH_OT_extrude_region={"mirror":False}, 
		TRANSFORM_OT_shrink_fatten={"value":0.2*radius})
	bpy.ops.object.mode_set(mode = 'OBJECT')

def Join () :
	for CurObj in bpy.context.scene.objects :
		if "Cylinder" in CurObj.name :
			CurObj.select = True
			bpy.context.scene.objects.active = CurObj
			bpy.ops.object.join()
			CurObj.name = "LogGroup"

def CreateLogGroup (x,y,z,radius) :
	logNumber = random.uniform(0,1)
	rotate = random.uniform(0,math.pi*2)
	CreateLog(x,y,z,radius)
	CreateLog(x,y+2*radius,z,radius)
	CreateLog(x,y+radius,z+1.5*radius,radius)
	if logNumber > 0.25 :
		CreateLog(x,y-2*radius,z,radius)
	if logNumber > 0.5 :
		CreateLog(x,y-radius,z+1.5*radius,radius)	
	if logNumber > 0.75 :
		CreateLog(x,y,z+3*radius,radius)
	Join()
	bpy.ops.transform.rotate(
		value=rotate, 
		axis=(0, 0, 1), 
		constraint_axis=(False, False, True))

def spawn_tonneau_entity(Xmin,Xmax,Ymin,Ymax):
	#bpy.ops.mesh.primitive_cube_add(radius=SCALE)
	imported_object = bpy.ops.import_scene.obj(filepath=str(dir_path+"/Tonneau.obj"))
	entity = bpy.context.selected_objects[0]
	entity.scale *= 0.5
	entity.name = "Tonneau" 
	#entity = bpy.context.scene.objects.active
	bpy.context.scene.objects.active = None
	bpy.ops.transform.translate(
		value=(random.uniform(Xmin,Xmax),random.uniform(Ymin,Ymax),0.5))

	return entity

def spawn_caisse_entity(Xmin,Xmax,Ymin,Ymax):
	#bpy.ops.mesh.primitive_cube_add(radius=SCALE)
	imported_object = bpy.ops.import_scene.obj(filepath=str(dir_path+"/Caisse.obj"))
	entity = bpy.context.selected_objects[0]
	entity.scale *= 0.5
	entity.name = "Caisse" 
	#entity = bpy.context.scene.objects.active
	bpy.context.scene.objects.active = None
	bpy.ops.transform.translate(
		value=(random.uniform(Xmin,Xmax),random.uniform(Ymin,Ymax),0.5))

	return entity

cleanAll()
radius = 0.2
bpy.context.scene.layers[0] = True
bpy.ops.mesh.primitive_plane_add(
	radius=10, 
	view_align=False, 
	enter_editmode=False, 
	location=(0, 0, 0))
for i in range (0,5) : 
	X = random.uniform(-5,5)
	Y = random.uniform(-5,5)
	CreateLogGroup(X,Y,radius,radius)
	spawn_tonneau_entity(-X,X,-Y,Y)
	spawn_caisse_entity(-X,X,-Y,Y)

newColor((0.0870936, 0.0187833, 0),"Log")
newColor((1, 0.510393, 0.229982),"CenterLog")

#Parcours de tout les objet
for obj in bpy.context.scene.objects :
	monObj = obj
	#Coloration de l'objet courant 
	monObj.select = True
	bpy.context.scene.objects.active = monObj
	if "LogGroup" in obj.name :
		setColorAll(monObj, "Log")
		bpy.ops.object.mode_set(mode = 'EDIT')
		# bpy.ops.mesh.select_face_by_sides(number=8, type='EQUAL')
		bpy.ops.object.material_slot_add()

		mat = bpy.data.materials.get("CenterLog")
		if mat is None:
		    # create material
		    mat = bpy.data.materials.new(name="Material")
		monObj.data.materials[1] = mat
		bpy.ops.object.material_slot_assign()
		bpy.ops.object.mode_set(mode = 'OBJECT')
	bpy.ops.rigidbody.object_add()
	bpy.context.object.rigid_body.friction = 1
	if "Plane" in obj.name:
		bpy.context.object.rigid_body.type = 'PASSIVE'	
	monObj.select = False



