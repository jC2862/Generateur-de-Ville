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

dir_path = os.path.dirname(__file__)
sys.path.append(dir_path+"/T")
import Particules
import Color
imp.reload(Particules)
imp.reload(Color)

planR = 10
density = 300

#Supprime tous les objets ainsi que toutes les data (particules, textures...)
def cleanAll():
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for bpy_data_iter in (bpy.data.objects,bpy.data.meshes,bpy.data.lamps,bpy.data.cameras,bpy.data.particles,bpy.data.materials,bpy.data.groups):
        for id_data in bpy_data_iter:
            bpy_data_iter.remove(id_data)

#permet d'obtenir seulement le cadre (les edges) d'une cellule selectionnée
def deleteCell () :
	bpy.ops.mesh.delete(type='ONLY_FACE')
	bpy.ops.mesh.select_mode(type = 'EDGE')
	bpy.ops.mesh.select_all(action='SELECT')

#fonction qui construit les trottoirs a partir du cadre (edges) d'une cellules de voronoi prealablement selectionnée
def makePavement () :
	bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0,0,0)})
	bpy.ops.transform.resize(value=(0.95, 0.95, 0.95))
	bpy.ops.mesh.select_all(action='SELECT')
	bpy.ops.mesh.extrude_region_move(
		TRANSFORM_OT_translate={"value":(0, 0, 0.02) })

#Chance le nom des objets selectionnée en "name"
def renameObject(name) :
	for obj in bpy.context.selected_objects:
		obj.name = name


"""MAIN"""

def execute() :
	cleanAll()
	start2 = time.time()
	routes, cells = J.execute()

	faces = []
	#Parcours de toutes les cellules de voronoi
	for Cell in cells :
		#Selection de la cellule courrante + faire en sorte que cette cellule soit l'objet actif
		Cell.select = True
		bpy.context.scene.objects.active = Cell
		me = bpy.context.object.data

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
	Particules.createParticulesBush ()

	#Changement render mode
	bpy.context.scene.render.engine = 'CYCLES'
	#Ajout d'une lampe
	bpy.ops.object.lamp_add(type='AREA', view_align=False, location=(0, 0, 4))

	#Redimension de l'ensemble de la scene 
	bpy.ops.object.select_all(action='SELECT')
	bpy.ops.transform.resize(value=(3, 3, 3))




























