import Utils
import bpy
import random

def fracturing(name):
    Utils.unselect()
    bpy.data.objects[name].select = True
    bpy.context.scene.objects.active = bpy.data.objects[name]
    bpy.ops.object.particle_system_add()
    PZ = bpy.context.scene.objects.active.particle_systems['ParticleSystem']
    PZ.seed = random.randint((-0x7fffffff - 1), 0x7fffffff)
    PA = PZ.settings
    PA.count = 60
    PA.frame_end = 2
    PA.distribution = 'RAND'
    bpy.ops.object.add_fracture_cell_objects(use_layer_next=False,use_debug_redraw=False)
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[name].select = True
    bpy.ops.object.particle_system_remove()
    #Suppression fracturing
    bpy.ops.object.delete(use_global=False)
    bpy.ops.object.select_all(action='TOGGLE')
    
def set_parent(child_name, parent_name):
    #Utils.unselect()
    bpy.data.objects[child_name].select = True
    bpy.data.objects[parent_name].select = True
    bpy.context.scene.objects.active = bpy.data.objects[parent_name]
    bpy.ops.object.parent_set( keep_transform=True)
    bpy.context.scene.objects.active = None
    bpy.data.objects[parent_name].select = False
    bpy.data.objects[child_name].select = False


def extra_voronoi():
    bpy.ops.view3d.snap_cursor_to_center()
    bpy.ops.wm.addon_enable(module="object_fracture_cell")
    bpy.ops.mesh.primitive_plane_add()
    bpy.ops.transform.resize(value=(10,10,0))
    base = bpy.context.active_object.name
    to_fusion = []

    fracturing(base)
    ABC = [obj for obj in bpy.context.scene.objects if obj.name.startswith(base+"_cell")]

    for a in ABC:
        Utils.unselect()
        a.select = True
        bpy.context.scene.objects.active = a
        '''''
        bpy.ops.object.duplicate_move()
        copie = bpy.context.scene.objects.active
        #to_fusion.append(copie.name)
        Utils.unselect()

        a.select = True
        bpy.context.scene.objects.active = a
        '''
        #abpy.ops.transform.resize(value=(0.90,0.90,0.90))
        to_fusion.append(a)
        bpy.ops.object.duplicate_move()
        bpy.ops.transform.resize(value=(0.82,0.82,0.82))
        '''
        fracturing(a.name)
        Z = [obj for obj in bpy.context.scene.objects if obj.name.startswith(a.name+"_cell")]
        for z in Z:
            Utils.unselect()
            z.select = True
            to_fusion.append(z)
            bpy.context.scene.objects.active = z
            bpy.ops.object.duplicate_move()
            bpy.ops.transform.resize(value=(0.82,0.82,0.82))
        '''
    
    Utils.unselect()
    for o in to_fusion:
        o.select = True 
    bpy.context.scene.objects.active = to_fusion[0]
    
    bpy.ops.object.join()
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.remove_doubles(threshold=0.01)
    bpy.ops.mesh.delete(type='ONLY_FACE')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.scene.objects.active.name = "Road"
    return bpy.context.scene.objects.active
    #bpy.ops.object.move_to_layer(layers=(False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))


    '''
        Utils.unselect()
        for z in Z:
            z.select = True
        bpy.context.scene.objects.active = Z[0]
        bpy.ops.transform.resize(value=(0.92,0.92,0.92))
    '''

    
    bpy.context.scene.objects.active = ABC[0]
    #bpy.ops.wm.addon_disable(module="object_fracture_cell")


def execute():
    return [extra_voronoi() , [obj for obj in bpy.context.scene.objects if obj.name.startswith("Plane_cell")]]