import bpy
import os
import sys
import imp
from mathutils import Vector

print("Entrée")
dir_path = os.path.dirname(__file__)
sys.path.append(dir_path+"/J")
import Voronoi
import Utils
imp.reload(Voronoi)
imp.reload(Utils)

def init_voronoi():
    V = Voronoi.Voronoi()
    cadre = Utils.creer_cadre(10)
    V.Sommets = cadre[0]
    V.Aretes = cadre[1]
    return V

def test_remplacement():
    V = init_voronoi()
    ancre = Vector((2,2))
    V.Ancres.append(ancre)
    V.Faces.append([ancre, V.Aretes])
    Z = V.Aretes[1]
    vec = Z[0] + (Z[1]-Z[0])*0.7
    V.Sommets.append(vec)
    V.remplacer(Z, [[Z[0],vec],[vec,Z[1]]])
    #Z = []
    return V

def test_intersection():
    V = init_voronoi()
    a1 = Vector((-7,-2))
    a2 = Vector((2,2))
    V.Ancres.append(a1)
    V.Ancres.append(a2)
    V.Faces.append([a1,V.Aretes])
    droite_millieux = Utils.creer_droite_milieux(a1, a2)
    #V.Aretes.append(droite_millieux)
    #V.Sommets.append(droite_millieux[0])
    #V.Sommets.append(droite_millieux[1])
    V.test_avec_ancre(a1, a2)
    print(V.conversion_Ancre(a1)[1])
    #Its = Utils.intersection([Vector((-10,10)),Vector((10,10))], droite_millieux)
    #V.Ancres.append(Its)
    #print(Its)
    return V

def lsystem():
    import Lsystem
    imp.reload(Lsystem)

    A = Vector((0,0))
    sommets.append(A)

def execute():
    lsystem()
    '''
    for i in range(5):
        print()
    #V = test_remplacement()
    V = test_intersection()
    #Conversion de l'objet
    ABC = V.conversion_Ancre(V.Ancres[0])
    mesh_data = bpy.data.meshes.new("cube_mesh_data")
    mesh_data.from_pydata(ABC[0], ABC[1], [])
    # création de l'objet contenant le mesh, et ajout à la scène
    obj = bpy.data.objects.new("Test", mesh_data)
    bpy.context.scene.objects.link(obj)
    '''    
    return