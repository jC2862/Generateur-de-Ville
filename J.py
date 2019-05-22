import os
import sys
import imp
import bpy 

dir_path = os.path.dirname(__file__)
sys.path.append(dir_path+"/J")
import Voronoi
import Utils
import RoadTruc
import Terrain
import CityBorder
imp.reload(Voronoi)
imp.reload(Utils)
imp.reload(RoadTruc)
imp.reload(Terrain)
imp.reload(CityBorder)

import T

def creer_route():
    return Voronoi.execute()

def creer_anim(road):
    RoadTruc.execute(road)

def execute():
    T.cleanAll()
    
    terrain = Terrain.generation(1000, 100)
    center = CityBorder.findPlaceIn(terrain)
    #road = bpy.context.scene.objects.active
    road, cellules = creer_route()
    bpy.ops.object.select_all(action='SELECT')
    terrain.select = False
    bpy.ops.transform.translate(value=(center.x, center.y, center.z+0.1),)
    creer_anim(road)
    return [road, cellules]
