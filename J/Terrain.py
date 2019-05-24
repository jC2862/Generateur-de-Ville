import bpy
from mathutils import Vector
from mathutils import noise
from math import acos
import random
import Utils

def getMaterial():
    for mat in bpy.data.materials:
        if mat.name == 'TerrainMaterial' :
            return mat
    mat = bpy.data.materials.new(name = 'TerrainMaterial')
    mat.use_nodes = True
    
    mat.node_tree.nodes.remove(mat.node_tree.nodes.get('Diffuse BSDF'))
    material_output = mat.node_tree.nodes.get('Material Output')
    ramp = mat.node_tree.nodes.new("ShaderNodeValToRGB")
    texcor = mat.node_tree.nodes.new("ShaderNodeTexCoord")
    xyz = mat.node_tree.nodes.new("ShaderNodeSeparateXYZ")
    toon = mat.node_tree.nodes.new("ShaderNodeBsdfToon")


    #ramp.color_ramp.elements.new(0.95)
    ramp.color_ramp.elements[0].color = [0.9,0.6,0.3,1]
    ramp.color_ramp.elements[1].position = 0.4
    ramp.color_ramp.elements[1].color = [0.04,0.2,0.04,1]
    #ramp.color_ramp.elements[2].color = [0.9,0.6,0.3,1]
    mat.node_tree.links.new(texcor.outputs['Object'], xyz.inputs[0])
    mat.node_tree.links.new(xyz.outputs['Z'], ramp.inputs[0])
    mat.node_tree.links.new(ramp.outputs['Color'], toon.inputs['Color'])
    mat.node_tree.links.new(toon.outputs['BSDF'], material_output.inputs["Surface"])

    #ramp = 


    return mat

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
    a = 20*pow(a,(1-a)*8)
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
    Utils.unselect()
    Utils.select(obj)
    bpy.ops.object.shade_smooth()
    mat = getMaterial()
    if mat != None : obj.data.materials.append(mat)
    Utils.unselect()
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
