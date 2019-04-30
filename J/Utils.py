from mathutils import Vector
import bpy

def allonger_arete(vec):
    ratio = 20/min(abs(vec.x), abs(vec.y))
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
