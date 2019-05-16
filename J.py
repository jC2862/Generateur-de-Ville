import os
import sys
import imp
import bpy 

dir_path = os.path.dirname(__file__)
sys.path.append(dir_path+"/J")
import Voronoi
import Utils
import RoadTruc
imp.reload(Voronoi)
imp.reload(Utils)
imp.reload(RoadTruc)

def creer_route():
    return Voronoi.execute()

def creer_anim(road):
    RoadTruc.execute(road)

def execute():
    #road, cellules = creer_route()
    creer_anim(bpy.data.objects["Road"])