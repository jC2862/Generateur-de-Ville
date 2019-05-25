import bpy
import bmesh
import random
import mathutils
import F    
import J
import time
import os
import sys
import imp
import Test

dir_path = os.path.dirname(__file__)
sys.path.append(dir_path+"/T")
import Particules
import StandGenerator
import Color
import Castle
imp.reload(Particules)
imp.reload(StandGenerator)
imp.reload(Color)
imp.reload(Castle)
imp.reload(J)

planR = 10
density = 300

#Supprime tous les objets ainsi que toutes les data (particules, textures...)
def cleanAll():
	# if len(bpy.data.objets) < 1:return
	bpy.ops.object.mode_set(mode = 'OBJECT')
	bpy.ops.object.select_all(action='SELECT')
	bpy.ops.object.delete(use_global=False)
	for bpy_data_iter in (bpy.data.objects,bpy.data.meshes,bpy.data.lamps,bpy.data.cameras,bpy.data.particles,bpy.data.materials,bpy.data.groups):
		for id_data in bpy_data_iter:
			bpy_data_iter.remove(id_data)

def renameObject(name) :
	for obj in bpy.context.selected_objects:
		obj.name = name

#permet d'obtenir seulement le cadre (les edges) d'une cellule selectionnée
def deleteCell () :
	bpy.ops.mesh.delete(type='ONLY_FACE')
	bpy.ops.mesh.select_mode(type = 'EDGE')
	bpy.ops.mesh.select_all(action='SELECT')

#fonction qui construit les trottoirs a partir du cadre (edges) d'une cellules de voronoi prealablement selectionnée
def makePavement () :
	bpy.ops.mesh.extrude_region_move(
		MESH_OT_extrude_region={"mirror":False}, 
		TRANSFORM_OT_translate={"value":(0, 0, 0.2), 
		"constraint_axis":(False, False, True), 
		"constraint_orientation":'GLOBAL', 
		"mirror":False, 
		"proportional":'DISABLED', 
		"proportional_edit_falloff":'SMOOTH',
		"proportional_size":1, 
		"snap":False, 
		"snap_target":'CLOSEST', 
		"snap_point":(0, 0, 0), 
		"snap_align":False, 
		"snap_normal":(0, 0, 0), 
		"gpencil_strokes":False, 
		"texture_space":False, 
		"remove_on_cancel":False, 
		"release_confirm":False, 
		"use_accurate":False})
	bpy.ops.transform.resize(value=(0.94, 0.94, 0.94))
	bpy.ops.transform.translate(
		value=(0, 0, -0.2), 
		constraint_axis=(False, False, True), 
		constraint_orientation='GLOBAL', 
		mirror=False, 
		proportional='DISABLED', 
		proportional_edit_falloff='SMOOTH', 
		proportional_size=1, 
		release_confirm=True, 
		use_accurate=False)
	bpy.ops.mesh.select_all(action='SELECT')
	bpy.ops.mesh.extrude_region_move(
		TRANSFORM_OT_translate={"value":(0, 0, 0.02) })

#Chance le nom des objets selectionnée en "name"
def renameObject(name) :
	for obj in bpy.context.selected_objects:
		obj.name = name


def CutTerrain () : 
	objects = bpy.data.objects
	cube = objects['CutCube']
	terrain = objects['Terrain']

	bool_one = terrain.modifiers.new(type="BOOLEAN", name="bool 1")
	bool_one.object = cube
	bool_one.operation = 'DIFFERENCE'
	terrain.select = True 
	bpy.context.scene.objects.active = terrain
	bpy.ops.object.modifier_apply(apply_as='DATA', modifier="bool 1")
	terrain.select = False 
	cube.select = True
	bpy.ops.object.delete(use_global=False)

"""MAIN"""

def execute() :
	cleanAll()
	Color.GenerateStandColors ()
	start2 = time.time()
	routes, cells = J.execute()

	faces = []
	#Parcours de toutes les cellules de voronoi
	for Cell in cells :
		#Selection de la cellule courrante + faire en sorte que cette cellule soit l'objet actif
		Cell.select = True
		bpy.context.scene.objects.active = Cell
		# print(Cell.name)
		bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
		# me = bpy.context.object.data

		#Duplication de la cellule courante qui permet ensuite de créer un trottoir
		bpy.ops.object.duplicate()
		renameObject("Pavement")
		bpy.ops.transform.resize(value=(1.05, 1.05, 1.05))
		bpy.ops.object.mode_set(mode = 'EDIT')
		deleteCell()
		makePavement()

		bpy.ops.object.mode_set(mode='OBJECT')
		bpy.ops.object.select_all(action='DESELECT')
	#Ajout d'un plan pour représenter la route
	bpy.ops.mesh.primitive_plane_add(radius=planR, location=(0, 0, -0.003))

	#Coloration de la route
	Color.ColorUnderRoad()
	#Creations de pierres sur la route
	Particules.createParticulesRock()
	#Coloration des cellules de Voronoi
	Color.ColorCells()
	#Creation des buissons sur les cellules de Voronoi (duplication de chaque cellules: voir fonction dans /T/Particules )
	freeCell = Particules.createParticulesOnCell ()

	#Changement render mode
	bpy.context.scene.render.engine = 'CYCLES'
	#Ajout d'une lampe
	# bpy.ops.object.lamp_add(type='AREA', view_align=False, location=(0, 0, 4))

	scaleValue = 3
	#Redimension de l'ensemble de la scene 
	bpy.ops.object.select_all(action='SELECT')
	bpy.ops.transform.resize(value=(scaleValue, scaleValue, scaleValue))

	# for obj in bpy.context.scene.objects :
	# 	rand = random.randint(0,1)
	# 	if "Plane_cell" in obj.name and rand == 1:
	# 		for vert in obj.verts

	for name in Particules.placeName :
		area = (bpy.context.scene.objects[name].dimensions[0] 
			+ bpy.context.scene.objects[name].dimensions[0]) / 2
		# print ("name : " + name + " area : "+ str(area))
		largeur = random.uniform(0.4,0.7)
		X=bpy.context.scene.objects[name].location[0]
		Y=bpy.context.scene.objects[name].location[1]
		if area > 5 : 
			StandGenerator.MakeStand (largeur*2, largeur, X, Y)

	print("CASTLE : " + Particules.GetBiggestCell())
	X=bpy.context.scene.objects[Particules.GetBiggestCell()].location[0]
	Y=bpy.context.scene.objects[Particules.GetBiggestCell()].location[1]
	DimX=bpy.context.scene.objects[Particules.GetBiggestCell()].dimensions[0]
	DimY=bpy.context.scene.objects[Particules.GetBiggestCell()].dimensions[1]
	Castle.MakeCastle(X,Y,0,DimX,DimY)


	bpy.ops.object.mode_set(mode='OBJECT')
	bpy.ops.object.select_all(action='DESELECT')
	test1=bpy.context.scene.objects["Plane"].location[0]
	test2=bpy.context.scene.objects["Plane"].location[1]
	bpy.ops.mesh.primitive_cube_add(radius=planR*scaleValue-0.5, location=(test1+0.1, test2+0.1, 0))
	renameObject("CutCube")
	
	CutTerrain()
	Particules.ParticulesOnTerrain()

	return freeCell






















