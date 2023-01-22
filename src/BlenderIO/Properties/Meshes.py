import bpy


class GFSToolsMeshProperties(bpy.types.PropertyGroup):
    def get_available_bones(self, context):
        armature = context.object.parent
        if armature is None:
            return []
        elif armature.type != "ARMATURE":
            return []
        else:
            bone_list = []
            for bpy_bone in armature.data.bones:
                bone_list.append((bpy_bone.name, bpy_bone.name, bpy_bone.name, "BONE_DATA", len(bone_list)))
            return bone_list

    reference_node: bpy.props.EnumProperty(items=get_available_bones, name="Reference Node")
    
    has_unknown_floats:  bpy.props.BoolProperty(name="Active")
    
    unknown_0x12:    bpy.props.FloatProperty(name="unknown 0x12")
    unknown_float_1: bpy.props.FloatProperty(name="unknown 1")
    unknown_float_2: bpy.props.FloatProperty(name="unknown 2")
    
    flag_5:  bpy.props.BoolProperty(name="Flag 5")
    flag_7:  bpy.props.BoolProperty(name="Flag 7")
    flag_8:  bpy.props.BoolProperty(name="Flag 8")
    flag_9:  bpy.props.BoolProperty(name="Flag 9")
    flag_10: bpy.props.BoolProperty(name="Flag 10")
    flag_11: bpy.props.BoolProperty(name="Flag 11")
    flag_13: bpy.props.BoolProperty(name="Flag 13")
    flag_14: bpy.props.BoolProperty(name="Flag 14")
    flag_15: bpy.props.BoolProperty(name="Flag 15")
    flag_16: bpy.props.BoolProperty(name="Flag 16")
    flag_17: bpy.props.BoolProperty(name="Flag 17")
    flag_18: bpy.props.BoolProperty(name="Flag 18")
    flag_19: bpy.props.BoolProperty(name="Flag 19")
    flag_20: bpy.props.BoolProperty(name="Flag 20")
    flag_21: bpy.props.BoolProperty(name="Flag 21")
    flag_22: bpy.props.BoolProperty(name="Flag 22")
    flag_23: bpy.props.BoolProperty(name="Flag 23")
    flag_24: bpy.props.BoolProperty(name="Flag 24")
    flag_25: bpy.props.BoolProperty(name="Flag 25")
    flag_26: bpy.props.BoolProperty(name="Flag 26")
    flag_27: bpy.props.BoolProperty(name="Flag 27")
    flag_28: bpy.props.BoolProperty(name="Flag 28")
    flag_29: bpy.props.BoolProperty(name="Flag 29")
    flag_30: bpy.props.BoolProperty(name="Flag 30")
    flag_31: bpy.props.BoolProperty(name="Flag 31")

