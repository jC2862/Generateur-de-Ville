import bpy
import bmesh
import math
import mathutils


class Sun :
    
    def __init__(self, lamp_name) :
        self.lamp = bpy.data.objects[lamp_name]
        print(self.lamp)
        self.lamp_euler = mathutils.Euler(self.lamp.rotation_euler, self.lamp.rotation_mode)
        self.vec = mathutils.Vector((0.0, 0.0, 1.0))
        
    def rotation(self) :
        self.vec.rotate(self.lamp_euler)  
        

class SkyMat :
    
    def __init__(self, sun, world, color=(0, 0, 0), turbidity = 2.2, albedo = .3) :
        world.use_nodes = True
        
        world_output = world.node_tree.nodes.get('World Output')
        
        bg = world.node_tree.nodes.new('ShaderNodeBackground')
        
        sky_tex = world.node_tree.nodes.new('ShaderNodeTexSky')
        sky_tex.outputs[0].default_value = color + (1, )
        sky_tex.sun_direction = sun.vec
        sky_tex.turbidity = turbidity
        sky_tex.ground_albedo = albedo
        
        world.node_tree.links.new(sky_tex.outputs[0], bg.inputs[0])
        world.node_tree.links.new(bg.outputs[0], world_output.inputs[0])
        self.material = world
        
def main(color=(0, 0, 0), turbidity = 2.2, albedo = .3) :
    world = bpy.data.worlds['World']
    sun = Sun('Sun')
    sun.rotation()
    print(sun.vec)
    sky = SkyMat(sun, world)    
            