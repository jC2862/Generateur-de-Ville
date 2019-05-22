import bpy
from mathutils import Vector
from mathutils import noise
from math import acos
import random


truc = random.randint(0,205465456)
#truc = 125436
#Terrain file -----------------------------------------------------------------------------------
def get_elevation(i,j,nbPointsLine):
    #Permet de modifier la variabilité du terrain
    mul = 4
    noise.seed_set(444576)
    a = noise.noise(Vector(
            ((i*mul)/nbPointsLine,
            (j*mul)/nbPointsLine,
            truc)))
    a=(1+a)/2
    a = 150*pow(a,(1-a)*6)
    #xa = pow(a,8)
    #a = 5 * (xa/(xa+0.002))
    return a 

#size: Largeur d'un coté du carré
#nbPointsLine: nombre de points par ligne
def create_terrain(size, nbPointsLine):
    sommets = []
    aretes = []
    faces = []

    diff = (size*1.) / (nbPointsLine*1.) 
    #Creation des sommets
    for i in range(nbPointsLine):
        for j in range(nbPointsLine):    
            sommets.append(
                [i*diff-(size/2),
                 j*diff-(size/2),
                 get_elevation(i,j,nbPointsLine)])
                 
    #Creation des faces
    # A  B
    # D  C
    for i in range(nbPointsLine-1):
        for j in range(nbPointsLine-1):
            A = nbPointsLine*i+j
            B = nbPointsLine*i+j+1
            C = nbPointsLine*(i+1)+j+1
            D = nbPointsLine*(i+1)+j
            faces.append([A,B,D])    
            faces.append([B,C,D])
    
    return [sommets, aretes, faces]
'''
size = 200
nbPointsLine = 100
'''
def generation(size, nbPointsLine):
    ret = create_terrain(size, nbPointsLine)
    #Generation terrain
    mesh_data = bpy.data.meshes.new("cube_mesh_data")
    mesh_data.from_pydata(ret[0], ret[1], ret[2])
    obj = bpy.data.objects.new("Terrain", mesh_data)
    bpy.context.scene.objects.link(obj)

    import random
    '''
    X = random.random()*size-size/2; Y = random.random()*size-size/2
    print("X:%lf Y:%lf" %(X,Y))

    #print(faces)

    mash_data = bpy.data.meshes.new("cube_mesh_data")
    mash_data.from_pydata([[X,Y,-2]], [], [])
    obj = bpy.data.objects.new("AZER", mash_data)
    bpy.context.scene.objects.link(obj)
    '''
    return obj
