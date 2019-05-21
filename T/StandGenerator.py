import bpy
import math 
import random
import Color

def MakePlot (x,y,height) :
	bpy.ops.mesh.primitive_cube_add(location=(x, y, height))
	bpy.ops.transform.resize(value=(0.02, 0.02, height))
	bpy.context.selected_objects[0].name = "TmpPlot"

def MakeRoof (longueur, largeur, x, y) :
	bpy.ops.mesh.primitive_plane_add(
		radius=1, 
		enter_editmode=True, 
		location=(x, y, 1) )
	bpy.ops.mesh.extrude_region_move(
		MESH_OT_extrude_region={"mirror":False}, 
		TRANSFORM_OT_translate={"value":(0, 0, 0.05), 
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
	bpy.context.selected_objects[0].name = "TmpRoof"

def PaintStand() :
	bpy.ops.object.mode_set(mode = 'OBJECT')
	bpy.ops.object.select_all(action='DESELECT')
	bpy.ops.object.select_pattern(pattern="TmpPlot*")
	for obj in bpy.context.selected_objects :
		Color.setColorAll(obj, "StandPole")
	bpy.ops.object.select_all(action='DESELECT')
	bpy.ops.object.select_pattern(pattern="TmpRoof*")
	i = random.randint(1,3)
	for obj in bpy.context.selected_objects :
		Color.setColorAll(obj, "StandColor"+str(i))

def MakeStand (longueur, largeur, x, y) :
	bpy.ops.object.select_all(action='DESELECT')
	MakeRoof(longueur, largeur, x, y)
	
	MakePlot(x+largeur,y+longueur,0.47)
	MakePlot(x+largeur,y+0,0.47)
	MakePlot(x+0,y+longueur,0.55)
	MakePlot(x+0,y+0,0.55)
	PaintStand()
	bpy.ops.object.select_all(action='DESELECT')
	bpy.ops.object.select_pattern(pattern="Tmp*")
	bpy.ops.object.join()
	bpy.context.selected_objects[0].name = "Stand"
	bpy.ops.transform.translate(
		value=(0, 0, 0.381453), 
		constraint_axis=(False, False, True))
	rotation = random.uniform(0,math.pi)
	bpy.ops.transform.rotate(
		value=rotation, 
		axis=(0, 0, 1), 
		constraint_axis=(True, True, False))

	print("test")
