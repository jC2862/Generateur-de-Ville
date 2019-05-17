import bpy
import bmesh
import random
import Utils
import math
from mathutils import Vector
from mathutils import Euler
from pathlib import Path

import os
#SCALE = 0.025
SCALE = 0.05
#Deplacement maximal pour 1 frames
VITESSE_DEPLACEMENT = 0.04

dir_path = os.path.dirname(__file__)

def init(road):
    Utils.unselect()
    road.select = True
    bpy.context.scene.objects.active = road
    bpy.ops.object.mode_set(mode='OBJECT')

def spawn_trafic_entity():
    #bpy.ops.mesh.primitive_cube_add(radius=SCALE)
    imported_object = bpy.ops.import_scene.obj(filepath=str(dir_path+"/../charette.obj"))
    entity = bpy.context.selected_objects[0]
    entity.scale *= SCALE
    entity.name = "Charette" 
    #entity = bpy.context.scene.objects.active
    bpy.context.scene.objects.active = None
    return entity

def spawn(nb_entities):
    bpy.ops.object.empty_add(type='PLAIN_AXES')
    trafic = bpy.context.scene.objects.active
    bpy.context.scene.objects.active.name = "Trafic"
    trafic.select = False
    bpy.context.scene.objects.active = None
    entities = []
    for i in range(nb_entities):
        entity = spawn_trafic_entity()
        print("APPEND: " + str(entity))
        entities.append(entity)
        Utils.set_parent(entity.name, "Trafic")
        bpy.context.scene.objects.active = None
    return entities

def other_vert_in_edge(edge, vert):
    return edge.verts[0] if edge.verts[0] != vert else edge.verts[1]

def iteration(cube, pre):
    #print("CUBE" + str(cube))
    ite = cube
    e = ite[0]
    edge = e.link_edges[random.randint(0,len(e.link_edges)-1)]
    prochain = other_vert_in_edge(edge, e)
    while prochain == pre:
        edge = e.link_edges[random.randint(0,len(e.link_edges)-1)]
        prochain = other_vert_in_edge(edge, e)
    dst = math.sqrt(Utils.distance2(e.co, prochain.co))
    nb_frame = int((dst/VITESSE_DEPLACEMENT)+0.5)
    future_frame = ite[1] + nb_frame
    #print(str(ite[1]) + " " + str(nb_frame) + " " + str(future_frame))
    #print("FUTURE FRAME : " + str(future_frame))
    return [prochain, future_frame]

def execute(road):
    init(road)
    matw = road.matrix_world
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(road.data)
    bm.verts.ensure_lookup_table()
    bm.edges.ensure_lookup_table()
    
    nb = bpy.data.scenes['Scene'].frame_end
    nb_cube = 10

    cubes = [[[bm.verts[random.randint(0,len(bm.verts)-1)],0]] for i in range(nb_cube)]
    print(cubes[0][0])

    #Calculs
    for cube in cubes:
        i=0
        while cube[i][1] < 250:
            to_append = iteration(cube[i], cube[i-1][0] if i > 0 else None)
            cube.append(to_append)
            i = i+1
    print(cubes[0])

    #Conversion
    CUBAS = []
    for cube in cubes:
        new_cube = []
        for i in range(len(cube)-1):
            cu = cube[i]
            vec = (cube[i+1][0].co-cube[i][0].co).normalized()
            print("VEC" + str(vec))
            rot = 0 
            if vec.x != 0 and vec.y != 0:
                rot = math.atan(vec.y/vec.x)
                rot += math.pi if vec.x < 0 else 0
            else:
                if vec.x != 0:
                    rot = vec.y * math.pi/2 
                elif vec.y !=0:
                    rot = vec.x * math.pi 
            new_cube.append([road.matrix_world * cu[0].co, (rot), cu[1]])
        cu = cube[len(cube)-1]
        new_cube.append([cu[0].co])
        CUBAS.append(new_cube)
    #Keycap
    bpy.ops.object.mode_set(mode='OBJECT')
    print(len(CUBAS))

    print(CUBAS[0][len(CUBAS[0])-1])

    entities = spawn(nb_cube)
    for i in range(len(CUBAS)):
        cube = CUBAS[i]
        print("LASTCUBE : "  + str(cube[len(cube)-1]))
        entity = entities[i]
        for j in range(len(cube)-1):
            entity.location = cube[j][0]
            #entity.rotation_euler = Euler((0,0,cube[j][1]))
            entity.rotation_euler.z = cube[j][1]
            entity.keyframe_insert(data_path="location", frame=cube[j][2])
            entity.keyframe_insert(data_path="rotation_euler", frame=cube[j][2]+2)
            #print(str(entity) + " " + str(cube[j]))
            if(cube[j][2] > 0):
                entity.rotation_euler.z = cube[j-1][1]
                entity.keyframe_insert(data_path="rotation_euler", frame=cube[j][2]-5)
                entity.keyframe_insert(data_path="location", frame=(cube[j][2]-1))
        entity.location = cube[len(cube)-1][0]
        entity.keyframe_insert(data_path="location", frame=(cube[j][2]))
        print(cube[len(cube)-1] )














