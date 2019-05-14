import bpy

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

#Coloration des buisson:
def ColorBush () :
	newColor((0.05,0.8,0.1),"Bush")
	#Parcours de tout les objet
	for obj in bpy.context.scene.objects :
		#Si l'objet est une Icosphere => c'est forcement un buisson
		if "Icosphere" in obj.name :
			monObj = obj
			#Coloration de l'objet courant 
			setColorAll(monObj, "Bush")


#Coloration des Cellules:
def ColorCells () :
	newColor((0.15,0.2,0.03),"Cell")
	#Parcours de tout les objet
	for obj in bpy.context.scene.objects :
		#Si l'objet est une plane_cell => c'est forcement une une cellule
		if "Plane_cell" in obj.name :
			monObj = obj
			#Coloration de l'objet courant 
			setColorAll(monObj, "Cell")


def ColorUnderRoad () :
	newColor((0.9,0.6,0.3),"UnderRoad")
	#Coloration de l'objet qui s'appelle "Plane" (plateforme sous qui represente les routes)
	monObj = bpy.context.scene.objects["Plane"]
	setColorAll(monObj, "UnderRoad")