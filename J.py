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
    
    terrain = Terrain.generation(250, 100)
    center = CityBorder.findPlaceIn(terrain)
    road, cellules = creer_route()
    creer_anim(road)
    
    bpy.ops.object.select_all(action='DESELECT')
    terrain.select = True
    bpy.ops.transform.translate(value=(-center.x, -center.y, center.z-0.01))
    return [road, cellules]
