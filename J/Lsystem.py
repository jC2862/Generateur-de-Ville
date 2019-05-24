print("azer")

import bpy
from mathutils import Vector
from mathutils import noise
import math
import random

sommets = []
aretes = []

def rotate(theta, vector):
    n_x = math.cos(theta)*vector.x - math.sin(theta)*vector.y
    n_y = math.sin(theta)*vector.x + math.cos(theta)*vector.y
    return Vector((n_x, n_y))
    
def distance(vecA, vecB):
    return math.sqrt(math.pow(vecB.x-vecA.x,2)+math.pow(vecB.y-vecA.y,2))

def appendAreteIfDifferent(A):
    if(A[0] != A[1]):
        aretes.append(A)

def conversion():
    conv = []
    global sommets
    global aretes
    for a in aretes:
        conv.append([sommets.index(a[0]), sommets.index(a[1])])
    aretes = conv
    conv = []
    for s in sommets:
        conv.append([s.x, s.y, 0])
    sommets = conv

#A: arete A
#B: arete B
def intersection(A,B):
    S1 = A[1]-A[0]
    S2 = B[1]-B[0]
    den = (-S2.x * S1.y + S1.x * S2.y)
    if(den == 0):
        return None    
    s = (-S1.y * (A[0].x - B[0].x) + S1.x * (A[0].y - B[0].y)) / den
    t = ( S2.x * (A[0].y - B[0].y) - S2.y * (A[0].x - B[0].x)) / den
    
#    s = (-S1.y * (A[0].x - B[0].x) + S1.x * (A[0].y - B[0].y)) / (-S2.x * S1.y + S1.x * S2.y)
#    t = ( S2.x * (A[0].y - B[0].y) - S2.y * (A[0].x - B[0].x)) / (-S2.x * S1.y + S1.x * S2.y)
    
    if(s>=0 and s<=1 and t>=0 and t<=1):
        return Vector((A[0].x+t*S1.x, A[0].y+t*S1.y))
    return None

def corriger_intersection(sommet_depart, dsc_inter):
    if(dsc_inter == None):return False
    
    sommets.append(dsc_inter[1])
    appendAreteIfDifferent([sommet_depart, dsc_inter[1]])
    appendAreteIfDifferent([dsc_inter[0][0], dsc_inter[1]])
    appendAreteIfDifferent([dsc_inter[0][1], dsc_inter[1]])
    aretes.remove(dsc_inter[0])
    return True

def sommet_equivalent(sommet):
    for s in sommets:
        if(distance(sommet, s) < 0.2):
            return s
    return None

def intersection_plus_proche(arete):
    #[arete_en_colision, intersection, distance]
    plus_proche = None
    for a in aretes:
        if(a[0] == arete[0] or a[1] == arete[0]):
            continue
        '''if(a[0].x - arete[0].x > 10 or a[1].y - arete[0].y > 10):
            continue'''
        it = intersection(arete, a) 
        if(it != None):
            dst = distance(arete[0], it)
            if(plus_proche == None or dst < plus_proche[2]):
                plus_proche = [a, it, dst]
    return plus_proche    

def ra():
    #return math.radians(30) + random.random() * math.radians(55)
    mul = 1 if random.random() > 0.5 else -1
    var = 3
    return (math.radians(var) + random.random() * math.radians(var*2))*mul

def iteration(precSommet, vecteur, level):
    if(level<1):
        return
    nouveau_sommet = precSommet + vecteur
    autre_sommet = sommet_equivalent(nouveau_sommet)
    if(autre_sommet!=None):
        aretes.append([precSommet, autre_sommet])
        return
    else:
        B = [precSommet, nouveau_sommet + vecteur*0.2]
        
        inte = intersection_plus_proche(B)
        if(inte != None):
            corriger_intersection(precSommet, inte)    
            return
        
    sommets.append(nouveau_sommet)
    appendAreteIfDifferent([precSommet, nouveau_sommet])
    #iteration(nouveau_sommet, rotate(+ra(), vecteur), level-1)
    #iteration(nouveau_sommet, rotate(-ra(), vecteur), level-1)
    iteration(nouveau_sommet, rotate(+ra(), vecteur), level-1)
    randominess = (1+noise.noise([precSommet.x/1000, precSommet.y/1000, 0]))/2
    if random.random() > 0.99:
        iteration(nouveau_sommet, rotate(math.radians(90), vecteur*0.9), level-1)

def create(vec, dir, level):
    #A = Vector((10,10))
    A = vec
    sommets.append(A)

    import time
    start = time.time()
    #iteration(A, Vector((0,2.5)), 50)
    iteration(A, dir, 120)
    end = time.time()

    print("Time %lf" %(end-start))

    # création du mesh
    conversion()
    mesh_data = bpy.data.meshes.new("cube_mesh_data")
    mesh_data.from_pydata(sommets, aretes, [])
    # création de l'objet contenant le mesh, et ajout à la scène
    obj = bpy.data.objects.new("Lsystem", mesh_data)
    bpy.context.scene.objects.link(obj)
    return obj
