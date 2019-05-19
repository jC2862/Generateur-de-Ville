import bpy
import random

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

def GenerateStandColors () :
	newColor((0.8,0.2,0.2),"StandColor1")
	newColor((0.2,0.8,0.2),"StandColor2")
	newColor((0.2,0.2,0.8),"StandColor3")
	newColor((0.517333, 0.310062, 0.133924),"StandPole")

#Coloration des buisson:
def ColorBush () :
	#Parcours de tout les objet
	i = 0
	for obj in bpy.context.scene.objects :
		ColorDif = random.uniform(0,0.2)
		colorName = "Bush" + str(i)
		newColor((0.05+ColorDif,0.8+ColorDif,0.1+ColorDif),colorName)
		#Si l'objet est une Icosphere => c'est forcement un buisson
		if "Icosphere" in obj.name :
			monObj = obj
			#Coloration de l'objet courant 
			setColorAll(monObj, colorName)
		i+=1

#Coloration des Cellules:
def ColorCells () :
	#Parcours de tout les objet
	i = 0
	for obj in bpy.context.scene.objects :
		ColorDif = random.uniform(0,0.1)
		colorName = "Cell" + str(i)
		newColor((0.15+ColorDif,0.2+ColorDif,0.03+ColorDif),colorName)
		#Si l'objet est une plane_cell => c'est forcement une une cellule
		if "Plane_cell" in obj.name :
			monObj = obj
			#Coloration de l'objet courant 
			setColorAll(monObj, colorName)
		i+=1


def ColorUnderRoad () :
	newColor((0.9,0.6,0.3),"UnderRoad")
	#Coloration de l'objet qui s'appelle "Plane" (plateforme sous qui represente les routes)
	monObj = bpy.context.scene.objects["Plane"]
	setColorAll(monObj, "UnderRoad")