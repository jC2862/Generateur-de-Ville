import bpy
import math 
import random
import os
import bmesh 

dir_path = os.path.dirname(__file__)

def cleanAll():
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for bpy_data_iter in (bpy.data.objects,bpy.data.meshes,bpy.data.lamps,bpy.data.cameras,bpy.data.particles,bpy.data.materials):
        for id_data in bpy_data_iter:
            bpy_data_iter.remove(id_data)

def spawn_part_entity():
    #bpy.ops.mesh.primitive_cube_add(radius=SCALE)
    imported_object = bpy.ops.import_scene.obj(filepath=str(dir_path+"/CastleBase.obj"))
    entity = bpy.context.selected_objects[0]
    entity.name = "Castle" 
    #entity = bpy.context.scene.objects.active
    bpy.context.scene.objects.active = None
    return entity

def spawn_tower_entity():
    #bpy.ops.mesh.primitive_cube_add(radius=SCALE)
    imported_object = bpy.ops.import_scene.obj(filepath=str(dir_path+"/Tower.obj"))
    entity = bpy.context.selected_objects[0]
    entity.name = "Tower" 
    #entity = bpy.context.scene.objects.active
    bpy.context.scene.objects.active = None
    return entity


def MakePart(longueur, largeur, hauteur, x, y, z) : 
	spawn_part_entity()
	bpy.ops.transform.resize(
		value=(longueur, largeur, hauteur), 
		constraint_axis=(False, False, False))
	bpy.ops.transform.translate(
		value=(x, y, 0))

	bpy.ops.object.select_all(action='DESELECT')

def MakeTower(hauteur,X,Y):
	spawn_tower_entity()
	bpy.ops.transform.resize(
		value=(1, 1, hauteur/4))
	bpy.ops.transform.translate(
		value=(X, Y, 0))



def MakeTowers(longueur,largeur,X,Y,hauteur):
	i = random.randint(0,1)
	hauteur = random.randint(4,6)
	MakeTower(hauteur,X+longueur-0.5,Y+largeur-0.5)
	MakeTower(hauteur,X-longueur+0.5,Y-largeur+0.5)

def MakeCastle(x,y,z,DimX,DimY) :
	nbPart = random.randint(3,6)
	X = 0
	Y = 0
	hauteur = 1
	for i in range(0,4) :
		Xr = random.choice([-1,1]) 
		Yr = random.choice([-1,1])
		X += Xr * 2 
		Y += Yr * 2
		longueur = random.randint(2,4) 
		largeur = random.randint(2,4) 
		hauteur += 0.5 
		MakePart(longueur,largeur,hauteur,X,Y,hauteur)
	MakeTowers(longueur,largeur,X,Y,hauteur)

	bpy.ops.object.select_all(action='DESELECT')
	bpy.ops.object.select_pattern(pattern="Castle*")
	bpy.ops.object.select_pattern(pattern="Tower*")
	bpy.context.scene.objects.active = bpy.context.scene.objects["Castle"]
	bpy.ops.object.join()
	# bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')
	bpy.ops.transform.resize(value=(0.7, 0.7, 1.3))
	bpy.context.object.dimensions[0] = DimX
	bpy.context.object.dimensions[1] = DimY
	DimZ = bpy.context.object.dimensions[2] 
	bpy.context.object.location[0] = x
	bpy.context.object.location[1] = y
	bpy.context.object.location[2] = 0.5


def execute () :
	cleanAll()
	# MakePart(1,1,1,0,0,0)
	MakeCastle(0,0,1.5)

