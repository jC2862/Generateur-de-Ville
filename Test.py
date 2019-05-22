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
    entity.name = "Part" 
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

def MakeCastle(x,y,z,size) :
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

	bpy.ops.object.select_all(action='SELECT')
	bpy.context.scene.objects.active = bpy.context.scene.objects["Part"]
	bpy.ops.object.join()

def execute () :
	cleanAll()
	# MakePart(1,1,1,0,0,0)
	MakeCastle(0,0,1.5,3)

