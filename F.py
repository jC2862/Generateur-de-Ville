import bpy
import bmesh
import os
import sys
import imp

def execute () :
	dir_path = os.path.dirname(__file__)
	sys.path.append(dir_path+"/F")

	import Main
	imp.reload(Main)

	#cree un grp de taille 2 * 2 (en forme de grille)
	n = Main.main()        