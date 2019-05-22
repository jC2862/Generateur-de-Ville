import bpy
import random
import Color
import os

dir_path = os.path.dirname(__file__)

def spawn_tonneau_entity():
	#bpy.ops.mesh.primitive_cube_add(radius=SCALE)
	imported_object = bpy.ops.import_scene.obj(filepath=str(dir_path+"/Tonneau.obj"))
	entity = bpy.context.selected_objects[0]
	entity.scale *= 0.5
	entity.name = "PlaceTonneau" 
	#entity = bpy.context.scene.objects.active
	bpy.context.scene.objects.active = None
	bpy.ops.transform.translate(
		value=(0,0,-2))

	return entity

def spawn_caisse_entity():
	#bpy.ops.mesh.primitive_cube_add(radius=SCALE)
	imported_object = bpy.ops.import_scene.obj(filepath=str(dir_path+"/Caisse.obj"))
	entity = bpy.context.selected_objects[0]
	entity.scale *= 0.5
	entity.name = "PlaceCaisse" 
	#entity = bpy.context.scene.objects.active
	bpy.context.scene.objects.active = None
	bpy.ops.transform.translate(
		value=(0,0,-2))

	return entity

def spawn_log_entity():
	#bpy.ops.mesh.primitive_cube_add(radius=SCALE)
	imported_object = bpy.ops.import_scene.obj(filepath=str(dir_path+"/LogGroup1.obj"))
	entity = bpy.context.selected_objects[0]
	entity.scale *= 0.5
	entity.name = "PlaceLog" 
	#entity = bpy.context.scene.objects.active
	bpy.context.scene.objects.active = None
	bpy.ops.transform.translate(
		value=(0,0,-2))

	return entity

def CreatePlaceGroup() :
	bpy.ops.object.mode_set(mode='OBJECT')	
	bpy.ops.object.select_all(action='DESELECT')
	spawn_tonneau_entity()
	spawn_log_entity()
	spawn_caisse_entity()
	bpy.ops.object.select_pattern(pattern="Place*")
	bpy.ops.group.create(name="Place")

#Création d'un groupe d'objet buisson
def createBush() : 
	for i in range(0,10) :
		bpy.ops.object.mode_set(mode='OBJECT')
		bpy.ops.object.select_all(action='DESELECT')
		BushRadius = 0.1
		#On créé une icosphere que l'on deforme un peu puis a laquelle on ajoute une couleur
		bpy.ops.mesh.primitive_ico_sphere_add(location=(0.0, 0.0, -1))
		bpy.ops.object.mode_set(mode='EDIT')
		bpy.ops.transform.vertex_random(offset=0.5)
		bpy.ops.mesh.vertices_smooth()
		Color.ColorBush()
	#on créé ensuite un groupe pour les buissons
	bpy.ops.object.mode_set(mode='OBJECT')
	bpy.ops.object.select_pattern(pattern="Icosphere*")
	bpy.ops.group.create(name="Bush")

#Creation d'un groupe d'objet pierre sur le meme foncitonnement que les buissons
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
	bpy.ops.group.create(name="Rock")

#application des particules de pierres sur l'objet "Plane"
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

	bpy.data.particles[lastPart].dupli_group = bpy.data.groups["Rock"]
	bpy.data.particles[lastPart].use_advanced_hair = True
	bpy.data.particles[lastPart].use_rotations = True
	#Permet de ne pas avoir des pierre verticales
	bpy.data.particles[lastPart].rotation_mode = 'OB_X'
	bpy.data.particles[lastPart].use_rotation_dupli = True

	bpy.data.particles[lastPart].particle_size = 0.15
	bpy.data.particles[lastPart].count = 500
	bpy.data.particles[lastPart].hair_length = 2.5
	bpy.data.particles[lastPart].size_random = 0.5
	bpy.context.object.particle_systems["ParticleSystem"].seed = random.randint(0,9999)

def renameObject(name) :
	for obj in bpy.context.selected_objects:
		obj.name = name

def createParticulesCell(obj, name, random_size, hair_length) :
	monObj = obj
	monObj.select = True
	bpy.context.scene.objects.active = monObj
	bpy.ops.object.duplicate()
	bpy.ops.transform.resize(value=(0.7, 0.7, 0.7))
	bpy.context.selected_objects[0].name = "Particles_Cell"
	area = bpy.context.object.data.polygons[0].area
	bpy.ops.object.particle_system_add()
	lastPart = len(bpy.data.particles) -1
	bpy.data.particles[lastPart].type = 'HAIR'
	bpy.data.particles[lastPart].render_type = 'GROUP'

	bpy.data.particles[lastPart].dupli_group = bpy.data.groups[name]
	bpy.data.particles[lastPart].use_advanced_hair = True
	bpy.data.particles[lastPart].use_rotations = True
	bpy.data.particles[lastPart].phase_factor = 0.5
	bpy.data.particles[lastPart].phase_factor_random = 2

	bpy.data.particles[lastPart].particle_size = 0.05
	bpy.data.particles[lastPart].count = area*2
	bpy.data.particles[lastPart].hair_length = hair_length
	bpy.data.particles[lastPart].size_random = random_size
	bpy.context.object.particle_systems["ParticleSystem"].seed = random.randint(0,9999)
	bpy.data.particles[lastPart].distribution = 'RAND'
	bpy.ops.object.select_all(action='DESELECT')

placeName = []
CastlePlace = "tmp"

def GetBiggestCell () :
	maxArea = 0
	for obj in bpy.context.scene.objects :
		area = (obj.dimensions[0] + obj.dimensions[1]) / 2
		if "Plane_cell" in obj.name :
			if area > maxArea :
				maxArea = area
				CastlePlace = obj.name
	return CastlePlace

#Application des particules de buissons sur tout les objets "plane_cell" (cellules de voronoi)
def createParticulesOnCell () :
	freeCell = []
	maxArea = 0
	createBush()
	CreatePlaceGroup()
	# bpy.ops.object.mode_set(mode='OBJECT')
	bpy.ops.object.select_all(action='DESELECT')
	for obj in bpy.context.scene.objects :
		rand = random.uniform(0,1)
		if "Plane_cell" in obj.name :
			freeCell.append(obj.name)
			area = (obj.dimensions[0] + obj.dimensions[1]) / 2
			if rand < 0.3:
				if area > maxArea :
					maxArea = area
					CastlePlace = obj.name
					print(CastlePlace + " < name / area > " + str(maxArea))		
				else : 
					createParticulesCell(obj, "Bush", 1, 2)
				freeCell.remove(obj.name)
			if rand > 0.8 :
				if area > maxArea :
					maxArea = area
					CastlePlace = obj.name
				else : 
					createParticulesCell(obj, "Place", 0, 1.5)
					placeName.append(obj.name)		
				freeCell.remove(obj.name)

	return freeCell