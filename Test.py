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

def MakePlot (x,y,height) :
	bpy.ops.mesh.primitive_cube_add(location=(x, y, height))
	bpy.ops.transform.resize(value=(0.1, 0.1, height))
	bpy.context.selected_objects[0].name = "StandPlot"

def MakeRoof (longueur, largeur, x, y) :
	bpy.ops.mesh.primitive_plane_add(
		radius=1, 
		enter_editmode=True, 
		location=(x, y, 2) )
	bpy.ops.mesh.extrude_region_move(
		MESH_OT_extrude_region={"mirror":False}, 
		TRANSFORM_OT_translate={"value":(0, 0, 0.2), 
		"constraint_axis":(False, False, True)})
	
	bpy.ops.object.mode_set(mode = 'OBJECT')
	bpy.ops.transform.resize(value=(largeur*1.1, longueur*0.75, 1))
	bpy.ops.transform.rotate(
		value=0.261818, 
		axis=(0, 1, 0), 
		constraint_axis=(True, False, True))
	bpy.ops.transform.translate(
		value=(largeur*0.4, 0, 0), 
		constraint_axis=(True, False, False))
	bpy.ops.transform.translate(
		value=(0, longueur*0.5, 0), 
		constraint_axis=(False, True, False))
	bpy.context.selected_objects[0].name = "StandRoof"



def MakeStand (longueur, largeur, x, y) :
	MakeRoof(longueur, largeur, x, y)
	
	MakePlot(x+largeur,y+longueur,1)
	MakePlot(x+largeur,y+0,1)
	MakePlot(x+0,y+longueur,1.1)
	MakePlot(x+0,y+0,1.1)
	bpy.ops.object.select_pattern(pattern="Stand*")
	bpy.ops.object.join()
	bpy.context.selected_objects[0].name = "Stand"



def execute () :
	cleanAll()
	bpy.ops.object.select_all(action='DESELECT')
	longueur = 3
	largeur = 1
	X = 2
	Y = 10
	MakeStand(longueur,largeur,X,Y)
