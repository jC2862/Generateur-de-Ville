import bpy
import bmesh
import random
import mathutils
import F    
import J
import time

planR = 10
density = 300

def cleanAll():
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for bpy_data_iter in (bpy.data.objects,bpy.data.meshes,bpy.data.lamps,bpy.data.cameras,bpy.data.particles,bpy.data.materials):
        for id_data in bpy_data_iter:
            bpy_data_iter.remove(id_data)


def setColorAll(obj, color):
    bpy.ops.object.mode_set(mode = 'OBJECT')
    if color not in obj.data.materials:
        obj.data.materials.append(bpy.data.materials[color])
    indexMat = obj.data.materials.find(color)
    for p in obj.data.polygons:
        obj.data.polygons[p.index].material_index = indexMat

def newColor(col, name):
    mat = bpy.data.materials.get(name)
    if mat == None:
        mat = bpy.data.materials.new(name)
    mat.diffuse_color = col
   
# def createRock() :
# 	X = random.uniform(-planR,planR)
# 	Y = random.uniform(-planR,planR)
# 	RockRadius = random.uniform(0,0.1)
# 	bpy.ops.mesh.primitive_cube_add(radius=RockRadius, location=(X, Y, 0))
# 	bpy.ops.object.modifier_add(type='SUBSURF')
# 	print("test")

def createBush() : 
	bpy.ops.object.mode_set(mode='OBJECT')
	bpy.ops.object.select_all(action='DESELECT')
	BushRadius = 0.1
	bpy.ops.mesh.primitive_ico_sphere_add(location=(0.0, 0.0, -1))
	bpy.ops.object.mode_set(mode='EDIT')
	bpy.ops.transform.vertex_random(offset=0.3)
	bpy.ops.mesh.vertices_smooth()
	ColorBush()
	bpy.ops.object.mode_set(mode='OBJECT')
	bpy.ops.object.select_pattern(pattern="Icosphere*")
	bpy.ops.group.create()

def ColorBush () :
	newColor((0.05,0.8,0.1),"Bush")
	print("test")
	for obj in bpy.context.scene.objects :
		if "Icosphere" in obj.name :
			monObj = obj
			setColorAll(monObj, "Bush")

def createRock() : 
	for i in range(0,10) :
		bpy.ops.object.mode_set(mode='OBJECT')
		bpy.ops.object.select_all(action='DESELECT')
		
		RockRadius = 0.2
		bpy.ops.mesh.primitive_cube_add(radius=RockRadius, location=(0, 0, -4))
		bpy.ops.transform.resize(value=(random.uniform(0.5,1), random.uniform(0.5,1), 0.3))
		bpy.ops.transform.rotate(
			value=random.uniform(0,10), 
			axis=(0, 0, 10), 
			)

		bpy.ops.object.modifier_add(type='SUBSURF')

		bpy.ops.object.mode_set(mode='EDIT')
	bpy.ops.object.mode_set(mode='OBJECT')
	bpy.ops.object.select_pattern(pattern="Cube*")
	bpy.ops.group.create()


def createParticulesRock () :
	createRock()

	bpy.ops.object.mode_set(mode='OBJECT')
	bpy.ops.object.select_all(action='DESELECT')
	bpy.context.scene.objects["Plane"].select = True
	bpy.context.scene.objects.active = bpy.context.scene.objects["Plane"]
	bpy.ops.object.particle_system_add()

	lastPart = len(bpy.data.particles) -1
	bpy.data.particles[lastPart].type = 'HAIR'
	bpy.data.particles[lastPart].render_type = 'GROUP'
	groupLen = len(bpy.data.groups) -1

	bpy.data.particles[lastPart].dupli_group = bpy.data.groups[groupLen]
	bpy.data.particles[lastPart].use_advanced_hair = True
	bpy.data.particles[lastPart].use_rotations = True
	bpy.data.particles[lastPart].rotation_mode = 'OB_X'
	bpy.data.particles[lastPart].use_rotation_dupli = True

	bpy.data.particles[lastPart].particle_size = 0.15
	bpy.data.particles[lastPart].count = 500
	bpy.data.particles[lastPart].hair_length = 2.5
	bpy.data.particles[lastPart].size_random = 0.5
	bpy.context.object.particle_systems["ParticleSystem"].seed = random.randint(0,9999)

def createParticulesBush () :
	createBush()

	bpy.ops.object.mode_set(mode='OBJECT')
	bpy.ops.object.select_all(action='DESELECT')
	for obj in bpy.context.scene.objects :
		rand = random.randint(0,1)
		if "Plane_cell" in obj.name and rand == 1:
			monObj = obj
			monObj.select = True
			bpy.context.scene.objects.active = monObj
			bpy.ops.object.duplicate()
			bpy.ops.transform.resize(value=(0.7, 0.7, 0.7))
			bpy.context.selected_objects[0].name = "test"
			area = bpy.context.object.data.polygons[0].area
			bpy.ops.object.particle_system_add()
			lastPart = len(bpy.data.particles) -1
			bpy.data.particles[lastPart].type = 'HAIR'
			bpy.data.particles[lastPart].render_type = 'GROUP'
			groupLen = len(bpy.data.groups) -1

			bpy.data.particles[lastPart].dupli_group = bpy.data.groups[groupLen]
			bpy.data.particles[lastPart].use_advanced_hair = True
			bpy.data.particles[lastPart].use_rotations = True
			bpy.data.particles[lastPart].phase_factor = 0.5
			bpy.data.particles[lastPart].phase_factor_random = 2

			bpy.data.particles[lastPart].particle_size = 0.05
			bpy.data.particles[lastPart].count = area
			bpy.data.particles[lastPart].hair_length = 2.5
			bpy.data.particles[lastPart].size_random = 1
			bpy.context.object.particle_systems["ParticleSystem"].seed = random.randint(0,9999)
			bpy.ops.object.select_all(action='DESELECT')

# def CutCells ():
# 	bpy.ops.object.mode_set(mode='OBJECT')
# 	bpy.ops.object.select_all(action='DESELECT')
# 	for obj in bpy.context.scene.objects :
# 		if "Plane_cell" in obj.name :
# 			monObj = obj
# 			monObj.select = True
# 			bpy.context.scene.objects.active = monObj
# 			bpy.ops.object.mode_set(mode='EDIT')
# 			bpy.ops.mesh.subdivide(number_cuts=6)
			# bpy.ops.object.modifier_add(type='DECIMATE')
			# bpy.ops.object.mode_set(mode='OBJECT')
			# bpy.context.object.modifiers["Decimate"].ratio = 0.5
			# bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Decimate")
			# bpy.ops.object.select_all(action='DESELECT')

def ColorCells () :
	newColor((0.15,0.2,0.03),"Cell")
	for obj in bpy.context.scene.objects :
		if "Plane_cell" in obj.name :
			monObj = obj
			setColorAll(monObj, "Cell")

def ColorUnderRoad () :
	newColor((0.9,0.6,0.3),"UnderRoad")
	monObj = bpy.context.scene.objects["Plane"]
	setColorAll(monObj, "UnderRoad")

def deleteCell () :
	bpy.ops.mesh.delete(type='ONLY_FACE')
	bpy.ops.mesh.select_mode(type = 'EDGE')
	bpy.ops.mesh.select_all(action='SELECT')

def makePavement () :
	bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0,0,0)})
	bpy.ops.transform.resize(value=(0.95, 0.95, 0.95))
	bpy.ops.mesh.select_all(action='SELECT')
	bpy.ops.mesh.extrude_region_move(
		TRANSFORM_OT_translate={"value":(0, 0, 0.02) })

def renameObject(name) :
	for obj in bpy.context.selected_objects:
		obj.name = name

cleanAll()
start2 = time.time()
J.execute()

faces = []
for CurObj in bpy.context.scene.objects :
	CurObj.select = True
	bpy.context.scene.objects.active = CurObj
	me = bpy.context.object.data
	bpy.ops.object.duplicate()

	renameObject("Pavement")

	bpy.ops.transform.resize(value=(1.05, 1.05, 1.05))

	bpy.ops.object.mode_set(mode = 'EDIT')

	deleteCell()

	makePavement()

	bpy.ops.object.mode_set(mode='OBJECT')
	bpy.ops.object.select_all(action='DESELECT')
bpy.ops.mesh.primitive_plane_add(radius=planR, location=(0, 0, -0.003))

ColorUnderRoad()
createParticulesRock()
ColorCells()
createParticulesBush ()

bpy.context.scene.render.engine = 'CYCLES'
bpy.ops.object.lamp_add(type='AREA', view_align=False, location=(0, 0, 4))

bpy.ops.object.select_all(action='SELECT')
bpy.ops.transform.resize(value=(3, 3, 3))

#decoupe routes WIP
# bpy.ops.view3d.viewnumpad(type='TOP')
# bpy.ops.object.select_all(action='SELECT')
# bpy.ops.object.mode_set(mode='EDIT')
# bpy.ops.mesh.knife_project()
# bpy.ops.object.mode_set(mode='OBJECT')
# bpy.ops.object.select_all(action='DESELECT')
# bpy.context.scene.objects["Plane"].select = True
# bpy.context.scene.objects.active = bpy.context.scene.objects["Plane"]




























