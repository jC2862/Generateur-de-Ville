from mathutils import Vector
import bpy
import random

def select(obj):
    obj.select = True
    bpy.context.scene.objects.active = obj

def remove(obj):
    unselect()
    select(obj)
    bpy.ops.object.delete(use_global=False)

def unselect():
    for obj in bpy.data.objects:
        obj.select = False

def distance2_3():
    pow(p2.x-p1.x,2) + pow(p2.y-p1.y,2) + pow(p2.z-p1.z,2)

def distance2(p1, p2):
    return pow(p2.x-p1.x,2) + pow(p2.y-p1.y,2)


def allonger_arete(vec):
    print(vec)
    X = abs(vec.x) if vec.x != 0 else abs(vec.y) 
    Y = abs(vec.y) if vec.y != 0 else abs(vec.x)
    ratio = 20/min(X, Y)
    return ratio * vec 

def rotate(theta, vector):
    n_x = math.cos(theta)*vector.x - math.sin(theta)*vector.y
    n_y = math.sin(theta)*vector.x + math.cos(theta)*vector.y
    return Vector((n_x, n_y))

def creer_cadre(SIZE):
    Sommets = []
    Aretes = []
    A = Vector((-SIZE,+SIZE))
    B = Vector((+SIZE,+SIZE))
    C = Vector((+SIZE,-SIZE))
    D = Vector((-SIZE,-SIZE))
    Sommets.append(A)
    Sommets.append(B)
    Sommets.append(C)
    Sommets.append(D)
    Aretes.append([A,B])
    Aretes.append([B,C])
    Aretes.append([C,D])
    Aretes.append([D,A])
    return [Sommets, Aretes]

def intersection(A,B):
    S1 = A[1]-A[0]
    S2 = B[1]-B[0]
    den = (-S2.x * S1.y + S1.x * S2.y)
    if(den == 0):
        return None    
    s = (-S1.y * (A[0].x - B[0].x) + S1.x * (A[0].y - B[0].y)) / den
    t = ( S2.x * (A[0].y - B[0].y) - S2.y * (A[0].x - B[0].x)) / den
    if(s>=0 and s<=1 and t>=0 and t<=1):
        return Vector((A[0].x+t*S1.x, A[0].y+t*S1.y))
    return None

def orthogonal(vector):
    n_x = -(1)*vector.y
    n_y = +(1)*vector.x
    return Vector((n_x, n_y))

def creer_droite_milieux(A, B):
    ortho = orthogonal(B-A)
    milieux_AB = (A+B)/2
    al = allonger_arete(ortho)
    C1 = milieux_AB + al
    C2 = milieux_AB - al
    return [C1,C2]

def getRandomPoint(SIZE):
    Bot_Lef = Vector((-SIZE,-SIZE))
    Up_Rig = Vector((+SIZE,+SIZE))
    Diag = Up_Rig - Bot_Lef
    return Bot_Lef + Vector((Diag.x*random.random(), Diag.y*random.random()))

def set_parent(child_name, parent_name):
    unselect()
    bpy.data.objects[child_name].select = True
    bpy.data.objects[parent_name].select = True
    bpy.context.scene.objects.active = bpy.data.objects[parent_name]
    bpy.ops.object.parent_set( keep_transform=True)
    bpy.context.scene.objects.active = None
    bpy.data.objects[parent_name].select = False
    bpy.data.objects[child_name].select = False