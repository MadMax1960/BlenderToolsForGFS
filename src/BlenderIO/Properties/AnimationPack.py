from collections import defaultdict

import bpy

from .Animations import poll_lookat_action
from ..modelUtilsTest.Misc.ID import new_unique_name
from .MixIns.Version import GFSVersionedProperty
from .GFSProperties import GFSToolsGenericProperty
from .Animations import BlobProperty, AnimBoundingBoxProps
from ..Utils.Animation import gapnames_from_nlatrack, gapnames_to_nlatrack, is_anim_restpose


class NLAStripWrapper(bpy.types.PropertyGroup):
    name:                bpy.props.StringProperty(name="Name", default="New Strip")
    frame_start_ui:      bpy.props.FloatProperty(default=1.)
    action_frame_start:  bpy.props.FloatProperty()
    action_frame_end:    bpy.props.FloatProperty()
    scale:               bpy.props.FloatProperty(default=1.)
    repeat:              bpy.props.FloatProperty(default=1.)
    action: bpy.props.PointerProperty(type=bpy.types.Action)

    def from_action(self, action):
        self.name                = action.name
        self.frame_start_ui      = 1.
        self.action_frame_start, \
        self.action_frame_end    = action.frame_range
        self.scale               = 1.
        self.repeat              = 1.
        self.action              = action

    def from_nla_strip(self, nla_strip):
        self.name                = nla_strip.name
        self.frame_start_ui      = nla_strip.frame_start_ui
        self.action_frame_start  = nla_strip.action_frame_start
        self.action_frame_end    = nla_strip.action_frame_end
        self.scale               = nla_strip.scale
        self.repeat              = nla_strip.repeat
        self.action              = nla_strip.action
    
    def to_nla_strip(self, nla_track):
        nla_strip = nla_track.strips.new(self.name,
                                         1,
                                         self.action)
        
        nla_strip.frame_start_ui     = self.frame_start_ui
        nla_strip.action_frame_start = self.action_frame_start
        nla_strip.action_frame_end   = self.action_frame_end
        nla_strip.scale              = self.scale
        nla_strip.repeat             = self.repeat


class NLATrackWrapper(bpy.types.PropertyGroup):
    name:   bpy.props.StringProperty(name="Name", default="New Track")
    strips: bpy.props.CollectionProperty(type=NLAStripWrapper)


class BaseTypedAnimation:
    obj_name: bpy.props.StringProperty(name="Name", default="")
    strips: bpy.props.CollectionProperty(type=NLAStripWrapper)

    def from_nla_track(self, nla_track, object_name):
        self.obj_name = object_name
        self.strips.clear()
        for nla_strip in nla_track.strips:
            prop_strip = self.strips.add()
            prop_strip.from_nla_strip(nla_strip)

    def to_nla_track(self, bpy_animation_data, gap_name, anim_type, anim_name):
        track = bpy_animation_data.nla_tracks.new()
        track.name = gapnames_to_nlatrack(gap_name, anim_type, anim_name)
        track.mute = True
        # Import strips in reverse start order so they don't bump into each
        # other when they get shifted to the correct position in the track
        for prop_strip in reversed(sorted(self.strips, key=lambda strip: strip.frame_start_ui)):
            prop_strip.to_nla_strip(track)


class NodeAnimationProperties(BaseTypedAnimation, bpy.types.PropertyGroup):
    compress: bpy.props.BoolProperty(name="Compress", default=True)

    def from_action(self, action):
        self.obj_name = ""
        self.strips.clear()
        prop_strip = self.strips.add()
        prop_strip.from_action(action)


class MaterialAnimationProperties(BaseTypedAnimation, bpy.types.PropertyGroup):
    pass


class CameraAnimationProperties(BaseTypedAnimation, bpy.types.PropertyGroup):
    pass


class Type4AnimationProperties(BaseTypedAnimation, bpy.types.PropertyGroup):
    pass


class MorphAnimationProperties(BaseTypedAnimation, bpy.types.PropertyGroup):
    pass


class AnimationProperties(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name")

    category: bpy.props.EnumProperty(items=[
            ("NORMAL",     "Normal",      "Standard Animation"                                             ),
            ("BLEND",      "Blend",       "Animations combined channel-by-channel with Standard Animations"),
            ("LOOKAT",     "Look At",     "Special Blend animations used for looking up/down/left/right"   )
        ],
        #update=update_category,
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
    
    bounding_box:    bpy.props.PointerProperty(type=AnimBoundingBoxProps)
    
    # Only for Normal animations
    has_lookat_anims:    bpy.props.BoolProperty(name="LookAt Anims")
    lookat_right:        bpy.props.StringProperty(name="LookAt Right", default="")
    lookat_left:         bpy.props.StringProperty(name="LookAt Left",  default="")
    lookat_up:           bpy.props.StringProperty(name="LookAt Up",    default="")
    lookat_down:         bpy.props.StringProperty(name="LookAt Down",  default="")
    lookat_right_factor: bpy.props.FloatProperty(name="LookAt Right Factor")
    lookat_left_factor:  bpy.props.FloatProperty(name="LookAt Left Factor")
    lookat_up_factor:    bpy.props.FloatProperty(name="LookAt Up Factor")
    lookat_down_factor:  bpy.props.FloatProperty(name="LookAt Down Factor")

    properties:          bpy.props.CollectionProperty(name="Properties", type=GFSToolsGenericProperty)
    active_property_idx: bpy.props.IntProperty(options={'HIDDEN'})

    # Animation Data
    has_blendscale_animation:  bpy.props.BoolProperty(name="Has Scale Animation")
    node_animation:            bpy.props.PointerProperty(type=NodeAnimationProperties)
    blendscale_node_animation: bpy.props.PointerProperty(type=NodeAnimationProperties)
    material_animations:       bpy.props.CollectionProperty(type=MaterialAnimationProperties)
    camera_animations:         bpy.props.CollectionProperty(type=CameraAnimationProperties)
    type4_animations:          bpy.props.CollectionProperty(type=Type4AnimationProperties)
    morph_animations:          bpy.props.CollectionProperty(type=MorphAnimationProperties)
    unimported_tracks:         bpy.props.StringProperty(name="HiddenUnimportedTracks", default="", options={"HIDDEN"})


class GFSToolsAnimationPackProperties(GFSVersionedProperty, bpy.types.PropertyGroup):
    is_active: bpy.props.BoolProperty(name="Active", default=False)
    name:    bpy.props.StringProperty(name="Name", default="New Pack")
    flag_0:  bpy.props.BoolProperty(name="Unknown Flag 0 (Unused?)")
    flag_1:  bpy.props.BoolProperty(name="Unknown Flag 1 (Unused?)")
    flag_3:  bpy.props.BoolProperty(name="Unknown Flag 3") # Enable morph anims?
    flag_4:  bpy.props.BoolProperty(name="Unknown Flag 4 (Unused?)")
    flag_5:  bpy.props.BoolProperty(name="Unknown Flag 5 (Unused?)")
    flag_6:  bpy.props.BoolProperty(name="Unknown Flag 6 (Unused?)")
    flag_7:  bpy.props.BoolProperty(name="Unknown Flag 7 (Unused?)")
    flag_8:  bpy.props.BoolProperty(name="Unknown Flag 8 (Unused?)")
    flag_9:  bpy.props.BoolProperty(name="Unknown Flag 9 (Unused?)")
    flag_10: bpy.props.BoolProperty(name="Unknown Flag 10 (Unused?)")
    flag_11: bpy.props.BoolProperty(name="Unknown Flag 11 (Unused?)")
    flag_12: bpy.props.BoolProperty(name="Unknown Flag 12 (Unused?)")
    flag_13: bpy.props.BoolProperty(name="Unknown Flag 13 (Unused?)")
    flag_14: bpy.props.BoolProperty(name="Unknown Flag 14 (Unused?)")
    flag_15: bpy.props.BoolProperty(name="Unknown Flag 15 (Unused?)")
    flag_16: bpy.props.BoolProperty(name="Unknown Flag 16 (Unused?)")
    flag_17: bpy.props.BoolProperty(name="Unknown Flag 17 (Unused?)")
    flag_18: bpy.props.BoolProperty(name="Unknown Flag 18 (Unused?)")
    flag_19: bpy.props.BoolProperty(name="Unknown Flag 19 (Unused?)")
    flag_20: bpy.props.BoolProperty(name="Unknown Flag 20 (Unused?)")
    flag_21: bpy.props.BoolProperty(name="Unknown Flag 21 (Unused?)")
    flag_22: bpy.props.BoolProperty(name="Unknown Flag 22 (Unused?)")
    flag_23: bpy.props.BoolProperty(name="Unknown Flag 23 (Unused?)")
    flag_24: bpy.props.BoolProperty(name="Unknown Flag 24 (Unused?)")
    flag_25: bpy.props.BoolProperty(name="Unknown Flag 25 (Unused?)")
    flag_26: bpy.props.BoolProperty(name="Unknown Flag 26 (Unused?)")
    flag_27: bpy.props.BoolProperty(name="Unknown Flag 27 (Unused?)")
    flag_28: bpy.props.BoolProperty(name="Unknown Flag 28 (Unused?)")
    flag_29: bpy.props.BoolProperty(name="Unknown Flag 29 (Unused?)")
    flag_30: bpy.props.BoolProperty(name="Unknown Flag 30 (Unused?)")
    flag_31: bpy.props.BoolProperty(name="Unknown Flag 31 (Unused?)")
    
    has_lookat_anims: bpy.props.BoolProperty(name="Has LookAt Anims")
    lookat_right:        bpy.props.PointerProperty(name="LookAt Right", type=bpy.types.Action, poll=poll_lookat_action)
    lookat_left:         bpy.props.PointerProperty(name="LookAt Left",  type=bpy.types.Action, poll=poll_lookat_action)
    lookat_up:           bpy.props.PointerProperty(name="LookAt Up",    type=bpy.types.Action, poll=poll_lookat_action)
    lookat_down:         bpy.props.PointerProperty(name="LookAt Down",  type=bpy.types.Action, poll=poll_lookat_action)
    lookat_right_factor: bpy.props.FloatProperty(name="LookAt Right Factor")
    lookat_left_factor:  bpy.props.FloatProperty(name="LookAt Left Factor")
    lookat_up_factor:    bpy.props.FloatProperty(name="LookAt Up Factor")
    lookat_down_factor:  bpy.props.FloatProperty(name="LookAt Down Factor")

    animations:            bpy.props.CollectionProperty(type=NLATrackWrapper)
    active_anim_idx:       bpy.props.IntProperty(default=-1)
    test_anims:            bpy.props.CollectionProperty(type=AnimationProperties)
    test_anims_idx:        bpy.props.IntProperty(default=-1)
    test_blend_anims:      bpy.props.CollectionProperty(type=AnimationProperties)
    test_blend_anims_idx:  bpy.props.IntProperty(default=-1)
    test_lookat_anims:     bpy.props.CollectionProperty(type=AnimationProperties)

    test_lookat_right:        bpy.props.StringProperty(name="LookAt Right", default="")
    test_lookat_left:         bpy.props.StringProperty(name="LookAt Left",  default="")
    test_lookat_up:           bpy.props.StringProperty(name="LookAt Up",    default="")
    test_lookat_down:         bpy.props.StringProperty(name="LookAt Down",  default="")

    ERROR_TEMPLATE = "CRITICAL INTERNAL ERROR: INVALID {msg} ANIMATION INDEX '{idx}'"

    def get_anim(self, idx, msg="list index out of range"):
        if not len(self.test_anims):
            return None
        elif idx == -1:
            return None
        elif idx < len(self.test_anims):
            return self.test_anims[idx]
        else:
            raise IndexError(msg)

    def _internal_get_anim(self, idx, msg):
        err_msg = self.ERROR_TEMPLATE.format(msg=msg, idx=idx)
        return self.get_anim(idx, err_msg)

    def get_selected_anim(self):
        return self._internal_get_anim(self.test_anims_idx, "SELECTED")

    def get_active_anim(self):
        return self._internal_get_anim(self.active_anim_idx, "ACTIVE")

    def store_animation_pack(self, bpy_armature_object):
        gap_props = self
        
        gap_props.animations.clear()
        if bpy_armature_object.animation_data is None:
            return

        for nla_track in bpy_armature_object.animation_data.nla_tracks:
            if is_anim_restpose(nla_track):
                continue
            
            prop_track = gap_props.animations.add()
            prop_track.name = nla_track.name
            
            for nla_strip in nla_track.strips:
                prop_strip = prop_track.strips.add()
                prop_strip.from_nla_strip(nla_strip)
    
    def restore_animation_pack(self, bpy_armature_object):
        gap_props = self
        
        self.remove_animations_from(bpy_armature_object)
        
        for prop_track in gap_props.animations:
            nla_track = bpy_armature_object.animation_data.nla_tracks.new()
            nla_track.name = prop_track.name
            nla_track.mute = True
            # Import strips in reverse start order so they don't bump into each
            # other when they get shifted to the correct position in the track
            for prop_strip in reversed(sorted(prop_track.strips, key=lambda strip: strip.frame_start_ui)):
                prop_strip.to_nla_strip(nla_track)

    @classmethod
    def remove_animations_from(cls, bpy_object):
        if bpy_object.animation_data is None:
            return
        
        ad = bpy_object.animation_data
        for nla_track in list(ad.nla_tracks):
            if is_anim_restpose(nla_track):
                continue
            
            ad.nla_tracks.remove(nla_track)
            
    def rename_unique(self, collection):
        self.name = new_unique_name(self.name, collection, separator=".")

    ###########
    # NEW API #
    ###########
    def is_track_tagged_as_this_pack(self, nla_track):
        gap_name, anim_type, anim_name = gapnames_from_nlatrack(nla_track)
        return gap_name == self.name

    def relevant_nla_to_list(self, bpy_object):
        if bpy_object.animation_data is None:
            return

        ad = bpy_object.animation_data
        valid_tracks = []
        names = defaultdict(lambda: 0)
        for nla_track in ad.nla_tracks:
            if self.is_track_tagged_as_this_pack(nla_track) and not is_anim_restpose(nla_track):
                valid_tracks.append(nla_track)
                names[nla_track.name] += 1

        # Data validation - make sure there are no duplicate tracks
        duplicate_tracks = {nm: count for nm, count in names.items() if count > 1}
        if len(duplicate_tracks):
            raise NotImplementedError("CRITICAL INTERNAL ERROR - UNIMPLEMENTED BEHAVIOUR - DUPLICATE NLA TRACK NAMES - POP UP A DIALOG HERE INSTEAD")

        return valid_tracks

    def anims_as_dict(self):
        out = {}
        for i, anim in enumerate(self.test_anims):
            out[anim.name] = anim
        return out

    def update_from_nla(self, bpy_object):
        if bpy_object.animation_data is None:
            return

        nla_tracks = self.relevant_nla_to_list(bpy_object)
        gap_anims  = self.anims_as_dict()

        # Now store the tracks on the GAP
        for nla_track in nla_tracks:
            _, _, anim_name = gapnames_from_nlatrack(nla_track)
            prop_anim = self.test_anims.add()
            prop_anim.name = anim_name
            prop_anim.node_animation.from_nla_track(nla_track, bpy_object.name)

            # TODO: BLENDSCALE ANIMS!!!!
            # blendscale_node_animation: bpy.props.PointerProperty(type=NodeAnimationProperties)

            if anim_name in gap_anims:
                gap_anim = gap_anims[anim_name]
                for elem in ["material_animations", "camera_animations", "type4_animations", "morph_animations"]:
                    gap_elems = getattr(gap_anim, elem)
                    prop_elems = getattr(prop_anim, elem)
                    for elem_anim in gap_elems:
                        prop_elem_anim = prop_elems.add()
                        prop_elem_anim.from_nla_track(elem_anim, elem_anim.name)
                prop_anim.unimported_tracks = gap_anim.unimported_tracks

        # Remove previous anims
        # Keep popping off front element
        for _ in range(len(gap_anims)):
            self.test_anims.remove(0)

        self.test_anims_idx = 0 if len(self.test_anims) else -1

    def remove_from_nla(self, bpy_object):
        if bpy_object.animation_data is None:
            return

        ad = bpy_object.animation_data
        for nla_track in list(ad.nla_tracks):
            if self.is_track_tagged_as_this_pack(nla_track) and not is_anim_restpose(nla_track):
                ad.nla_tracks.remove(nla_track)

    def add_to_nla(self, bpy_object):
        if bpy_object.animation_data is None:
            bpy_object.animation_data_create()

        ad = bpy_object.animation_data
        for prop_anim in self.test_anims:
            prop_anim.node_animation.to_nla_track(ad, self.name, prop_anim.category, prop_anim.name)
