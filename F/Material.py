import bpy
import colorsys
from random import randint

class ColorGenerator :
    
    def hsv_to_rgb(self, h, s, v):
        if s == 0.0: return (v, v, v)
        i = int(h*6.) # XXX assume int() truncates!
        f = (h*6.)-i; p,q,t = v*(1.-s), v*(1.-s*f), v*(1.-s*(1.-f)); i%=6
        if i == 0: return (v, t, p)
        if i == 1: return (q, v, p)
        if i == 2: return (p, v, t)
        if i == 3: return (p, q, v)
        if i == 4: return (t, p, v)
        if i == 5: return (v, p, q)
    
    def __init__(self, type) :
        if type == 'Wall' :
            self.col = self.init_color((15, 25), (0, 35), (50, 75))
        elif type == 'Roof' :
            self.col = self.init_color((0, 30), (60, 101), (40, 60))
        elif type == 'Glass' :     
            print("Euhhhhhhhhhhhhhh pas normal")
            self.col = self.init_color((210, 220), (80, 101), (80, 101))
        elif type == 'Frame' :
            self.col = self.init_color((0, 20), (50, 76), (25, 60))
        else :
            self.col = self.init_color((0, 1), (0, 1), (0, 1))      

    def init_color(self, h, s, v) :
        hue = randint(h[0], h[1])
        saturation = randint(s[0], s[1])/100
        value = randint(v[0], v[1])/100
        #print("hue : {}, sat : {}, val : {}".format(hue, saturation, value))
        a = colorsys.hsv_to_rgb(hue, saturation, value)
        b = colorsys.rgb_to_hsv(a[0], a[1], a[2])
        c = colorsys.hsv_to_rgb(b[0], b[1], b[2])
        print("rgb :", a)
        print("hsv :", b)
        print("rgb :", c)
        return a

class ToonMaterial :
    
    def __init__(self, name, color=(0, 0, 0), hue=.5, saturation=1.0, value=.8, fac=1.0, size_0=.6, smooth_0=.2, size_1=.3, smooth_1=.02) :
        mat = bpy.data.materials.new(name = name)
        mat.use_nodes = True
        
        #remove default node 
        mat.node_tree.nodes.remove(mat.node_tree.nodes.get('Diffuse BSDF'))
        #get output location
        material_output = mat.node_tree.nodes.get('Material Output')
        
        #Dans l'ordre logique des choses :
        
        #notre couleur d'entree
        rgb = mat.node_tree.nodes.new('ShaderNodeRGB')
        #sucre syntaxique depython pour concatener deux "tuples"
        rgb.outputs[0].default_value = color + (1, )
        print(rgb.outputs[0].default_value[0])
        print(rgb.outputs[0].default_value[1])
        print(rgb.outputs[0].default_value[2])
        print(rgb.outputs[0].default_value[3])
        
        #on va utiliser deux Toon BSDF Diffus de couleurs differentes (ombre stylise)
        #on va lier nos materiaux convenablement 
        toon_0 = mat.node_tree.nodes.new('ShaderNodeBsdfToon')
        mat.node_tree.links.new(rgb.outputs[0], toon_0.inputs[0])
        toon_0.inputs[1].default_value = size_0
        toon_0.inputs[2].default_value = smooth_0
        
        toon_1 = mat.node_tree.nodes.new('ShaderNodeBsdfToon') 
        hue_sat = mat.node_tree.nodes.new('ShaderNodeHueSaturation')
        hue_sat.inputs[0].default_value = hue
        hue_sat.inputs[1].default_value = saturation
        hue_sat.inputs[2].default_value = value
        hue_sat.inputs[3].default_value = fac
        mat.node_tree.links.new(rgb.outputs[0], hue_sat.inputs[4]) 
        mat.node_tree.links.new(hue_sat.outputs[0], toon_1.inputs[0])
        toon_1.inputs[1].default_value = size_1
        toon_1.inputs[2].default_value = smooth_1    
        
        #on va ajouter nos deux shaders 
        add = mat.node_tree.nodes.new('ShaderNodeAddShader') 
        mat.node_tree.links.new(add.inputs[0], toon_0.outputs[0])    
        mat.node_tree.links.new(add.inputs[1], toon_1.outputs[0])
        
        #enfin on connecte a la sortie
        mat.node_tree.links.new(add.outputs[0], material_output.inputs[0])
        print(rgb.outputs[0].default_value[0])
        print(rgb.outputs[0].default_value[1])
        print(rgb.outputs[0].default_value[2])
        print(rgb.outputs[0].default_value[3])
        
        self.material = mat
        
#shadre = Toon_Material("Nom", color=(0.1, 0.2, 0.45))      

def affect_mat(obj, name,  type) :
    color = ColorGenerator(type)
    toon = ToonMaterial(name, color.col)   
    obj.data.materials.append(toon.material)
    
#affect([], 'Wall')    
#obj = bpy.data.objects['64']
#affect_mat(obj, "Frame_mat", 'Frame')