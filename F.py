import bpy
import bmesh
import os
import sys
import imp

def execute () :
	dir_path = os.path.dirname(__file__)
	sys.path.append(dir_path+"/F")

	import Neighbourhood
	imp.reload(Neighbourhood)

	#cree un grp de taille 2 * 2 (en forme de grille)
	n = Neighbourhood.Neighbourhood(2, 2)        
	res = n.create_neighbourhood()        
	n.to_group("Neighborhood", res)
	bpy.ops.object.mode_set(mode = 'OBJECT') 
