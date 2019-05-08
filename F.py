import bpy
import bmesh
import os
import sys
import imp

def execute () :
	dir_path = os.path.dirname(__file__)
	sys.path.append(dir_path+"/F")

	import HouseGenerator
	imp.reload(HouseGenerator)

	do = HouseGenerator.main()
	bpy.ops.object.mode_set(mode = 'OBJECT') 