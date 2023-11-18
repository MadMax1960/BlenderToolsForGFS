import bpy
from .HelpWindows import defineHelpWindow
from .Model import OBJECT_PT_GFSToolsModelDataPanel
from ..Preferences import get_preferences

from ..modelUtilsTest.UI.UIList import UIListBase
from ..Globals import NAMESPACE


class SwitchAnimation(bpy.types.Operator):
    index: bpy.props.IntProperty()

    bl_label   = ""
    bl_idname = f"{NAMESPACE}.switchanimation"
    bl_options = {"UNDO", "REGISTER"}

    @classmethod
    def poll(cls, context):
        bpy_armature_object = context.active_object
        mprops = bpy_armature_object.data.GFSTOOLS_ModelProperties
        return mprops.is_selected_gap_active()

    def execute(self, context):
        bpy_armature_object = context.active_object
        anim_data           = bpy_armature_object.animation_data
        mprops = bpy_armature_object.data.GFSTOOLS_ModelProperties
        gap = mprops.get_selected_gap()

        name = f"{gap.name}_{gap.test_anims[self.index].name}"

        # Reset armature pose, deactivate tracks
        for nla_track in anim_data.nla_tracks:
            nla_track.mute = True
        for bone in bpy_armature_object.pose.bones:
            bone.location            = (0., 0., 0.)
            bone.rotation_quaternion = (1., 0., 0., 0.)
            bone.rotation_euler      = (0., 0., 0.)
            bone.scale               = (1., 1., 1.)

        # Reactivate any necessary animations, set index
        if gap.active_anim_idx == self.index:
            gap.active_anim_idx = -1
        else:
            gap.active_anim_idx = self.index
            for nla_track in anim_data.nla_tracks:
                if nla_track.name == name or nla_track.name == "Rest Pose":
                    nla_track.mute = False

        return {'FINISHED'}


class OBJECT_UL_GFSToolsAnimationUIList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index, flt_flag):
        bpy_armature_object = context.active_object
        mprops = bpy_armature_object.data.GFSTOOLS_ModelProperties
        gap = mprops.get_selected_gap()

        icon_name = "SOLO_ON" if index == gap.active_anim_idx else "SOLO_OFF"
        op = layout.operator(SwitchAnimation.bl_idname, icon=icon_name, emboss=False)
        op.index = index
        layout.prop(item, "name", text="", emboss=False)


_uilist = UIListBase(
    NAMESPACE,
    "GAPAnims",
    OBJECT_UL_GFSToolsAnimationUIList,
    "test_anims",
    "test_anims_idx",
    lambda ctx: ctx.armature.GFSTOOLS_ModelProperties.get_selected_gap(),
    extra_collection_indices=["active_anim_idx"]
)
setattr(_uilist, "poll", classmethod(lambda cls, context: get_preferences().developer_mode))


class OBJECT_PT_GFSToolsAnimationPackDataPanel(bpy.types.Panel):
    bl_label       = "GFS Animation Pack"
    bl_parent_id   = OBJECT_PT_GFSToolsModelDataPanel.bl_idname
    bl_idname      = "OBJECT_PT_GFSToolsAnimationPackDataPanel"
    bl_space_type  = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context     = "data"
    bl_options     = {'DEFAULT_CLOSED'}

    ANIM_LIST = _uilist()

    @classmethod
    def poll(self, context):
        if context.armature is None:
            return False
        
        bpy_armature = context.armature
        mprops = bpy_armature.GFSTOOLS_ModelProperties
        if mprops.get_selected_gap() is None:
            return False
        
        return True

    def draw(self, context):
        bpy_armature = context.armature
        mprops = bpy_armature.GFSTOOLS_ModelProperties
        
        layout = self.layout
        
        layout.operator(self.AnimationPackHelpWindow.bl_idname)
        
        props = mprops.get_selected_gap()
        
        layout.prop(props, 'version')
        # Flags
        flag_col = layout.column()
        flag_col.prop(props, "flag_0")
        flag_col.prop(props, "flag_1")
        flag_col.prop(props, "flag_3")
        flag_col.prop(props, "flag_4")
        flag_col.prop(props, "flag_5")
        flag_col.prop(props, "flag_6")
        flag_col.prop(props, "flag_7")
        flag_col.prop(props, "flag_8")
        flag_col.prop(props, "flag_9")
        flag_col.prop(props, "flag_10")
        flag_col.prop(props, "flag_11")
        flag_col.prop(props, "flag_12")
        flag_col.prop(props, "flag_13")
        flag_col.prop(props, "flag_14")
        flag_col.prop(props, "flag_15")
        flag_col.prop(props, "flag_16")
        flag_col.prop(props, "flag_17")
        flag_col.prop(props, "flag_18")
        flag_col.prop(props, "flag_19")
        flag_col.prop(props, "flag_20")
        flag_col.prop(props, "flag_21")
        flag_col.prop(props, "flag_22")
        flag_col.prop(props, "flag_23")
        flag_col.prop(props, "flag_24")
        flag_col.prop(props, "flag_25")
        flag_col.prop(props, "flag_26")
        flag_col.prop(props, "flag_27")
        flag_col.prop(props, "flag_28")
        flag_col.prop(props, "flag_29")
        flag_col.prop(props, "flag_30")
        flag_col.prop(props, "flag_31")
        
        # LookAts
        flag_col.prop(props, "has_lookat_anims")
        lookat_col = layout.column()
        lookat_col.prop(props, "lookat_up")
        lookat_col.prop(props, "lookat_up_factor")
        lookat_col.prop(props, "lookat_down")
        lookat_col.prop(props, "lookat_down_factor")
        lookat_col.prop(props, "lookat_left")
        lookat_col.prop(props, "lookat_left_factor")
        lookat_col.prop(props, "lookat_right")
        lookat_col.prop(props, "lookat_right_factor")
        
        lookat_col.enabled = props.has_lookat_anims

        if get_preferences().developer_mode:
            self.ANIM_LIST.draw(layout, context)

    AnimationPackHelpWindow = defineHelpWindow("AnimationPack",
        "- 'Unknown Flags' are unknown. Only Flag 3 appears to be used and may do something.\n"\
        "- 'LookAt Anims' are a set of animations for the four directions the character can look in.\n"\
    )
            
    @classmethod
    def register(cls):
        bpy.utils.register_class(cls.AnimationPackHelpWindow)
        bpy.utils.register_class(SwitchAnimation)
        bpy.utils.register_class(OBJECT_UL_GFSToolsAnimationUIList)
        _uilist.register()
    
    @classmethod
    def unregister(cls):
        bpy.utils.unregister_class(cls.AnimationPackHelpWindow)
        bpy.utils.unregister_class(SwitchAnimation)
        bpy.utils.unregister_class(OBJECT_UL_GFSToolsAnimationUIList)
        _uilist.unregister()
