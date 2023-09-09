import bpy

from .GFSProperties import GFSToolsGenericProperty
from .Nodes import BlobProperty
from ..modelUtilsTest.Mesh.Prebuilts import make_cuboid
from ..Utils.PhysicsGen import get_col_material


def update_bounding_box_mesh(props, context):
    mesh_name = props.bounding_box_name()
    if mesh_name not in bpy.data.objects:
        return
    
    bpy_mesh_object = bpy.data.objects[mesh_name]
    bpy_mesh = bpy_mesh_object.data
            
    dims = [mx - mn for mx, mn in zip(props.bounding_box_max, props.bounding_box_min)]
    ctr = [(mx + mn)/2 for mx, mn in zip(props.bounding_box_max, props.bounding_box_min)]

    bpy_mesh_object.lock_location[0] = False
    bpy_mesh_object.lock_location[1] = False
    bpy_mesh_object.lock_location[2] = False
    bpy_mesh_object.location = ctr
    bpy_mesh_object.lock_location[0] = True
    bpy_mesh_object.lock_location[1] = True
    bpy_mesh_object.lock_location[2] = True
    
    bpy_mesh.clear_geometry()
    bpy_mesh.from_pydata(*make_cuboid(*dims, [1, 1, 1]))


def update_category(self, context):
    if context.active_nla_strip is None:
        return
    
    strip = context.active_nla_strip
    action = strip.action
    props = action.GFSTOOLS_AnimationProperties
    
    if props.autocorrect_action:
        for fc in action.fcurves:
            if fc.datapath.endswith("rotation_quaternion"):
                for k in fc.keyframe_points:
                    k.interpolation = "BEZIER"
            else:
                for k in fc.keyframe_points:
                    k.interpolation = "LINEAR"
        if props.category == "NORMAL":
            strip.blend_type = "REPLACE"
        elif props.category in {"BLEND", "LOOKAT"}:
            strip.blend_type = "COMBINE"
        elif props.category == "BLENDSCALE":
            strip.blend_type = "ADD"


def poll_blendscale_action(self, action):
    return action.GFSTOOLS_AnimationProperties.category == "BLENDSCALE"

 
def poll_lookat_action(self, action):
    return action.GFSTOOLS_AnimationProperties.category == "LOOKAT"
    

class GFSToolsAnimationProperties(bpy.types.PropertyGroup):   
    def bounding_box_name(self):
        return f".GFS_{self.id_data.name}"
    
    def generate_bounding_box(self):
        props = self
        
        dims = [mx - mn for mx, mn in zip(props.bounding_box_max, props.bounding_box_min)]
        ctr = [(mx + mn)/2 for mx, mn in zip(props.bounding_box_max, props.bounding_box_min)]
        
        nm = self.bounding_box_name()
        bpy_mesh = bpy.data.meshes.new(nm)
        bpy_mesh.from_pydata(*make_cuboid(*dims, [1, 1, 1]))
        bpy_mesh_object = bpy.data.objects.new(nm, bpy_mesh)
        bpy.context.collection.objects.link(bpy_mesh_object)
        bpy_mesh_object.location = ctr
        
        bpy_mesh_object.lock_location[0] = True
        bpy_mesh_object.lock_location[1] = True
        bpy_mesh_object.lock_location[2] = True
        
        bpy_mesh_object.lock_rotation[0] = True
        bpy_mesh_object.lock_rotation[1] = True
        bpy_mesh_object.lock_rotation[2] = True
        bpy_mesh_object.lock_rotation_w  = True
        
        bpy_mesh_object.lock_scale[0]    = True
        bpy_mesh_object.lock_scale[1]    = True
        bpy_mesh_object.lock_scale[2]    = True
        
        bpy_mesh_object.active_material = get_col_material()
        
    
    def remove_bounding_box(self):
        objs = bpy.data.objects
        nm = self.bounding_box_name()
        if nm in objs:
            objs.remove(objs[nm], do_unlink=True)
    
    autocorrect_action: bpy.props.BoolProperty(name="Auto-correct Actions", 
                                               description="Automatically set the keyframe interpolation and strip blending that will show how the animations looks in-game when selecting a category for the animation",
                                               default=False)
    category: bpy.props.EnumProperty(items=[
            ("NORMAL",     "Normal",      "Standard Animation"                                             ),
            ("BLEND",      "Blend",       "Animations combined channel-by-channel with Standard Animations"),
            ("BLENDSCALE", "Blend Scale", "Scale animations to be added to a Standard Animation scale"     ),
            ("LOOKAT",     "Look At",     "Special Blend animations used for looking up/down/left/right"   )
        ],
        update=update_category,
        name="Category"
    )

    epls:                bpy.props.CollectionProperty(name="EPLs",
                                                      type=BlobProperty,
                                                      options={'HIDDEN'})
    
    # Common properties
    flag_0:  bpy.props.BoolProperty(name="Unknown Flag 0", default=True) # Enable node anims?
    flag_1:  bpy.props.BoolProperty(name="Unknown Flag 1", default=False) # Enable material anims?
    flag_2:  bpy.props.BoolProperty(name="Unknown Flag 2", default=False) # Enable camera anims?
    flag_3:  bpy.props.BoolProperty(name="Unknown Flag 3", default=False) # Enable morph anims?
    flag_4:  bpy.props.BoolProperty(name="Unknown Flag 4", default=False) # Enable type 5 anims?
    flag_5:  bpy.props.BoolProperty(name="Unknown Flag 5 (Unused?)", default=False)
    flag_6:  bpy.props.BoolProperty(name="Unknown Flag 6 (Unused?)", default=False)
    flag_7:  bpy.props.BoolProperty(name="Unknown Flag 7 (Unused?)", default=False)
    flag_8:  bpy.props.BoolProperty(name="Unknown Flag 8 (Unused?)", default=False)
    flag_9:  bpy.props.BoolProperty(name="Unknown Flag 9 (Unused?)", default=False)
    flag_10: bpy.props.BoolProperty(name="Unknown Flag 10 (Unused?)", default=False)
    flag_11: bpy.props.BoolProperty(name="Unknown Flag 11 (Unused?)", default=False)
    flag_12: bpy.props.BoolProperty(name="Unknown Flag 12 (Unused?)", default=False)
    flag_13: bpy.props.BoolProperty(name="Unknown Flag 13 (Unused?)", default=False)
    flag_14: bpy.props.BoolProperty(name="Unknown Flag 14 (Unused?)", default=False)
    flag_15: bpy.props.BoolProperty(name="Unknown Flag 15 (Unused?)", default=False)
    flag_16: bpy.props.BoolProperty(name="Unknown Flag 16 (Unused?)", default=False)
    flag_17: bpy.props.BoolProperty(name="Unknown Flag 17 (Unused?)", default=False)
    flag_18: bpy.props.BoolProperty(name="Unknown Flag 18 (Unused?)", default=False)
    flag_19: bpy.props.BoolProperty(name="Unknown Flag 19 (Unused?)", default=False)
    flag_20: bpy.props.BoolProperty(name="Unknown Flag 20 (Unused?)", default=False)
    flag_21: bpy.props.BoolProperty(name="Unknown Flag 21 (Unused?)", default=False)
    flag_22: bpy.props.BoolProperty(name="Unknown Flag 22 (Unused?)", default=False)
    flag_24: bpy.props.BoolProperty(name="Unknown Flag 24 (Unused?)", default=False)
    flag_26: bpy.props.BoolProperty(name="Unknown Flag 26 (Unused?)", default=False)
    flag_27: bpy.props.BoolProperty(name="Unknown Flag 27 (Unused?)", default=False)
    
    export_bounding_box: bpy.props.BoolProperty(name="Export Bounding Box", default=False)
    bounding_box_min:    bpy.props.FloatVectorProperty(name="Bounding Box Min", size=3, default=(0, 0, 0), update=update_bounding_box_mesh)
    bounding_box_max:    bpy.props.FloatVectorProperty(name="Bounding Box Max", size=3, default=(0, 0, 0), update=update_bounding_box_mesh)
    
    unimported_tracks: bpy.props.StringProperty(name="HiddenUnimportedTracks", default="", options={"HIDDEN"})
    
    # Only for Normal animations
    has_lookat_anims:    bpy.props.BoolProperty(name="LookAt Anims")
    lookat_right:        bpy.props.PointerProperty(name="LookAt Right", type=bpy.types.Action, poll=poll_lookat_action)
    lookat_left:         bpy.props.PointerProperty(name="LookAt Left",  type=bpy.types.Action, poll=poll_lookat_action)
    lookat_up:           bpy.props.PointerProperty(name="LookAt Up",    type=bpy.types.Action, poll=poll_lookat_action)
    lookat_down:         bpy.props.PointerProperty(name="LookAt Down",  type=bpy.types.Action, poll=poll_lookat_action)
    lookat_right_factor: bpy.props.FloatProperty(name="LookAt Right Factor")
    lookat_left_factor:  bpy.props.FloatProperty(name="LookAt Left Factor")
    lookat_up_factor:    bpy.props.FloatProperty(name="LookAt Up Factor")
    lookat_down_factor:  bpy.props.FloatProperty(name="LookAt Down Factor")
    
    # Only for Blend and LookAt animations
    has_scale_action:   bpy.props.BoolProperty(name="Has Scale Channel")
    blend_scale_action: bpy.props.PointerProperty(name="Scale Channel", type=bpy.types.Action, poll=poll_blendscale_action)

    properties:          bpy.props.CollectionProperty(name="Properties", type=GFSToolsGenericProperty)
    active_property_idx: bpy.props.IntProperty(options={'HIDDEN'})
