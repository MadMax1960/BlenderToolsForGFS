import bpy
from ..Utils.UVMapManagement import is_valid_uv_map, get_uv_idx_from_name

def gen_tex_prop(name, getter=None):
    description = "" if getter is None else "This UV map is determined from the appropriate node in the shader tree"
    return bpy.props.EnumProperty(name=name, items=[
            ("None", "None", "Unused UV channel"),
            ("0", "UV0", "Use UV0"),
            ("1", "UV1", "Use UV1"),
            ("2", "UV2", "Use UV2"),
            ("3", "UV3", "Use UV3"),
            ("4", "UV4", "Use UV4"),
            ("5", "UV5", "Use UV5"),
            ("6", "UV6", "Use UV6")
        ], default="None", description=description, get=getter)


def get_in_tex(self, name):
    material = self.id_data
    if material.node_tree is None:
        return 0
    
    nodes = material.node_tree.nodes
    if name not in nodes:
        return 1

    tex_node = nodes[name]
    if tex_node.type != "TEX_IMAGE":
        return 0
    connections = tex_node.inputs["Vector"].links

    tex_idx = None
    if len(connections):
        uv_node = connections[0].from_socket.node
        if uv_node.type == "UVMAP":
            uv_map_name = uv_node.uv_map
            if is_valid_uv_map(uv_map_name):
                proposed_tex_idx = get_uv_idx_from_name(uv_map_name)
                if proposed_tex_idx < 7:
                    tex_idx = proposed_tex_idx
                    return tex_idx + 1
    
    return "UV0"


class GFSToolsTextureRefPanelProperties(bpy.types.PropertyGroup):
    # def update_unknown_0x04(self, context):
    #     print("UPDATING")
    
    enable_anims: bpy.props.BoolProperty(name="Animatable", default=False)#update=update_unknown_0x04)
    unknown_0x08: bpy.props.BoolProperty(default=True)
    has_texture_filtering: bpy.props.BoolProperty(name="Filter Texture", default=True)
    unknown_0x0A: bpy.props.IntProperty(default=0) # 0, 1, 2
    unknown_0x0B: bpy.props.IntProperty(default=0) # 0, 1, 2
    unknown_0x0C: bpy.props.FloatProperty(default=1.) # -1, 0, 1, 1.3, 2, 5
    unknown_0x10: bpy.props.FloatProperty(default=-0.) # -1, 0
    unknown_0x14: bpy.props.FloatProperty(default=0.)
    unknown_0x18: bpy.props.FloatProperty(default=0.)
    unknown_0x1C: bpy.props.FloatProperty(default=0.) # 0, 1
    unknown_0x20: bpy.props.FloatProperty(default=1.) # -1, 0, 1, 2, 4, 5
    unknown_0x24: bpy.props.FloatProperty(default=0.)
    unknown_0x28: bpy.props.FloatProperty(default=0.)
    unknown_0x2C: bpy.props.FloatProperty(default=0.)
    unknown_0x30: bpy.props.FloatProperty(default=0.)
    unknown_0x34: bpy.props.FloatProperty(default=0.)
    unknown_0x38: bpy.props.FloatProperty(default=0.)
    unknown_0x3C: bpy.props.FloatProperty(default=0.)
    unknown_0x40: bpy.props.FloatProperty(default=0.)
    unknown_0x44: bpy.props.FloatProperty(default=0.)
    unknown_0x48: bpy.props.FloatProperty(default=0.)



class GFSToolsMaterialProperties(bpy.types.PropertyGroup):
    flag_0:          bpy.props.BoolProperty(name="Unknown Flag 0",       default=True )
    flag_1:          bpy.props.BoolProperty(name="Unknown Flag 1",       default=True )
    enable_specular: bpy.props.BoolProperty(name="Enable Specular",      default=False)
    flag_3:          bpy.props.BoolProperty(name="Unknown Flag 3",       default=False)
    vertex_colors:   bpy.props.BoolProperty(name="Enable Vertex Colors", default=False)
    flag_5:          bpy.props.BoolProperty(name="Unknown Flag 5",       default=True )
    flag_6:          bpy.props.BoolProperty(name="Unknown Flag 6",       default=False)
    enable_uv_anims: bpy.props.BoolProperty(name="Enable UV Anims",      default=False)
    enable_emissive: bpy.props.BoolProperty(name="Enable Emissive",      default=False)
    flag_9:          bpy.props.BoolProperty(name="Unknown Flag 9",       default=False)
    flag_10:         bpy.props.BoolProperty(name="Unknown Flag 10",      default=False)
    light_2:         bpy.props.BoolProperty(name="Use Light 2",          default=True )
    pwire:           bpy.props.BoolProperty(name="Purple Wireframe",     default=False)
    flag_13:         bpy.props.BoolProperty(name="Unknown Flag 13",      default=False)
    receive_shadow:  bpy.props.BoolProperty(name="Receive Shadow",       default=False)
    cast_shadow:     bpy.props.BoolProperty(name="Cast Shadow",          default=False)
    flag_18:         bpy.props.BoolProperty(name="Unknown Flag 18",      default=False)
    disable_bloom:   bpy.props.BoolProperty(name="Disable Bloom",        default=False)
    flag_29:         bpy.props.BoolProperty(name="Unknown Flag 29",      default=False)
    flag_30:         bpy.props.BoolProperty(name="Unknown Flag 30",      default=False)
    flag_31:         bpy.props.BoolProperty(name="Unknown Flag 31",      default=False)
    
    ambient:         bpy.props.FloatVectorProperty(name="Ambient Color",  size=4, default=(1., 1., 1., 1.))
    diffuse:         bpy.props.FloatVectorProperty(name="Diffuse Color",  size=4, default=(1., 1., 1., 1.))
    specular:        bpy.props.FloatVectorProperty(name="Specular Color", size=4, default=(1., 1., 1., 1.))
    emissive:        bpy.props.FloatVectorProperty(name="Emissive Color", size=4, default=(1., 1., 1., 1.))
    reflectivity:    bpy.props.FloatProperty      (name="Reflectivity",   default=0.)
    outline_idx:     bpy.props.FloatProperty      (name="Outline Idx.",   default=0.)
    draw_method:     bpy.props.IntProperty        (name="Draw Method",    default=0, min=0, max=65535) # Change to enum later
    unknown_0x51:    bpy.props.IntProperty        (name="Unknown 0x51",   default=0, min=0, max=65535)
    unknown_0x52:    bpy.props.IntProperty        (name="Unknown 0x52",   default=0, min=0, max=65535)
    unknown_0x53:    bpy.props.IntProperty        (name="Unknown 0x53",   default=0, min=0, max=65535)
    unknown_0x54:    bpy.props.IntProperty        (name="Unknown 0x54",   default=0, min=0, max=65535)
    unknown_0x55:    bpy.props.IntProperty        (name="Unknown 0x55",   default=1, min=0, max=65536) # Change to enum later
    unknown_0x56:    bpy.props.IntProperty        (name="Unknown 0x56",   default=0, min=0, max=65535) # Some kind of 8-bit flag?!
    unknown_0x58:    bpy.props.IntProperty        (name="Unknown 0x58",   default=0, min=0, max=65535) # Change to enum later?
    unknown_0x5A:    bpy.props.IntProperty        (name="Unknown 0x5A",   default=1, min=-32768, max=32767) # Flags?
    unknown_0x5C:    bpy.props.IntProperty        (name="Unknown 0x5C",   default=0, min=-32768, max=32767) # Flags?
    unknown_0x5E:    bpy.props.IntProperty        (name="Unknown 0x5E",   default=0, min=-32768, max=32767) # Flags?
    unknown_0x6A:    bpy.props.IntProperty        (name="Unknown 0x6A",   default=-1, min=-2147483648, max=2147483647) # Always -1

    # Required vertex attributes
    requires_normals:   bpy.props.BoolProperty(name="Requires Normals",      default=True )
    requires_tangents:  bpy.props.BoolProperty(name="Requires Tangents",     default=False)
    requires_binormals: bpy.props.BoolProperty(name="Requires Binormals",    default=False)
    requires_color0s:   bpy.props.BoolProperty(name="Requires Color Map 0 ", default=False)
    requires_color1s:   bpy.props.BoolProperty(name="Requires Color Map 1",  default=False)
    # Positions?
    # Weights?
    
    diffuse_uv_in:     gen_tex_prop("", lambda self: get_in_tex(self, "Diffuse Texture"))
    diffuse_uv_out:    gen_tex_prop("")
    normal_uv_in:      gen_tex_prop("", lambda self: get_in_tex(self, "Normal Texture"))
    normal_uv_out:     gen_tex_prop("")
    specular_uv_in:    gen_tex_prop("", lambda self: get_in_tex(self, "Specular Texture"))
    specular_uv_out:   gen_tex_prop("")
    reflection_uv_in:  gen_tex_prop("", lambda self: get_in_tex(self, "Reflection Texture"))
    reflection_uv_out: gen_tex_prop("")
    highlight_uv_in:   gen_tex_prop("", lambda self: get_in_tex(self, "Highlight Texture"))
    highlight_uv_out:  gen_tex_prop("")
    glow_uv_in:        gen_tex_prop("", lambda self: get_in_tex(self, "Glow Texture"))
    glow_uv_out:       gen_tex_prop("")
    night_uv_in:       gen_tex_prop("", lambda self: get_in_tex(self, "Night Texture"))
    night_uv_out:      gen_tex_prop("")
    detail_uv_in:      gen_tex_prop("", lambda self: get_in_tex(self, "Detail Texture"))
    detail_uv_out:     gen_tex_prop("")
    shadow_uv_in:      gen_tex_prop("", lambda self: get_in_tex(self, "Shadow Texture"))
    shadow_uv_out:     gen_tex_prop("")
    
    ##################
    # TOON ATTRIBUTE #
    ##################
    
    has_toon:  bpy.props.BoolProperty(name="Active")
    
    toon_colour:           bpy.props.FloatVectorProperty(name="Color", default=[1., 1., 1., 1.], size=4)
    toon_light_threshold:  bpy.props.FloatProperty(name="Light Threshold")
    toon_light_factor:     bpy.props.FloatProperty(name="Light Factor")
    toon_light_brightness: bpy.props.FloatProperty(name="Light Brightness")
    toon_shadow_threshold: bpy.props.FloatProperty(name="Shadow Threshold")
    toon_shadow_factor:    bpy.props.FloatProperty(name="Shadow Factor")
    
    toon_ctr_flag_0:  bpy.props.BoolProperty(name="Unknown Attr. Flag 0",  default=True)
    toon_ctr_flag_1:  bpy.props.BoolProperty(name="Unknown Attr. Flag 1  (Unused?)",  default=False)
    toon_ctr_flag_2:  bpy.props.BoolProperty(name="Unknown Attr. Flag 2  (Unused?)",  default=False)
    toon_ctr_flag_3:  bpy.props.BoolProperty(name="Unknown Attr. Flag 3  (Unused?)",  default=False)
    toon_ctr_flag_4:  bpy.props.BoolProperty(name="Unknown Attr. Flag 4  (Unused?)",  default=False)
    toon_ctr_flag_5:  bpy.props.BoolProperty(name="Unknown Attr. Flag 5  (Unused?)",  default=False)
    toon_ctr_flag_6:  bpy.props.BoolProperty(name="Unknown Attr. Flag 6  (Unused?)",  default=False)
    toon_ctr_flag_7:  bpy.props.BoolProperty(name="Unknown Attr. Flag 7  (Unused?)",  default=False)
    toon_ctr_flag_8:  bpy.props.BoolProperty(name="Unknown Attr. Flag 8  (Unused?)",  default=False)
    toon_ctr_flag_9:  bpy.props.BoolProperty(name="Unknown Attr. Flag 9  (Unused?)",  default=False)
    toon_ctr_flag_10: bpy.props.BoolProperty(name="Unknown Attr. Flag 10 (Unused?)", default=False)
    toon_ctr_flag_11: bpy.props.BoolProperty(name="Unknown Attr. Flag 11 (Unused?)", default=False)
    toon_ctr_flag_12: bpy.props.BoolProperty(name="Unknown Attr. Flag 12 (Unused?)", default=False)
    toon_ctr_flag_13: bpy.props.BoolProperty(name="Unknown Attr. Flag 13 (Unused?)", default=False)
    toon_ctr_flag_14: bpy.props.BoolProperty(name="Unknown Attr. Flag 14 (Unused?)", default=False)
    toon_ctr_flag_15: bpy.props.BoolProperty(name="Unknown Attr. Flag 15 (Unused?)", default=False)
    
    toon_flag_0:  bpy.props.BoolProperty(name="Unknown Flag 0",            default=True)
    toon_flag_1:  bpy.props.BoolProperty(name="Unknown Flag 1",            default=False)
    toon_flag_2:  bpy.props.BoolProperty(name="Unknown Flag 2",            default=False)
    toon_flag_3:  bpy.props.BoolProperty(name="Unknown Flag 3",            default=False)
    toon_flag_4:  bpy.props.BoolProperty(name="Unknown Flag 4",            default=False)
    toon_flag_5:  bpy.props.BoolProperty(name="Unknown Flag 5",            default=False)
    toon_flag_6:  bpy.props.BoolProperty(name="Unknown Flag 6",            default=False)
    toon_flag_7:  bpy.props.BoolProperty(name="Unknown Flag 7  (Unused?)", default=False)
    toon_flag_8:  bpy.props.BoolProperty(name="Unknown Flag 8  (Unused?)", default=False)
    toon_flag_9:  bpy.props.BoolProperty(name="Unknown Flag 9  (Unused?)", default=False)
    toon_flag_10: bpy.props.BoolProperty(name="Unknown Flag 10 (Unused?)", default=False)
    toon_flag_11: bpy.props.BoolProperty(name="Unknown Flag 11 (Unused?)", default=False)
    toon_flag_12: bpy.props.BoolProperty(name="Unknown Flag 12 (Unused?)", default=False)
    toon_flag_13: bpy.props.BoolProperty(name="Unknown Flag 13 (Unused?)", default=False)
    toon_flag_14: bpy.props.BoolProperty(name="Unknown Flag 14 (Unused?)", default=False)
    toon_flag_15: bpy.props.BoolProperty(name="Unknown Flag 15 (Unused?)", default=False)
    toon_flag_16: bpy.props.BoolProperty(name="Unknown Flag 16 (Unused?)", default=False)
    toon_flag_17: bpy.props.BoolProperty(name="Unknown Flag 17 (Unused?)", default=False)
    toon_flag_18: bpy.props.BoolProperty(name="Unknown Flag 18 (Unused?)", default=False)
    toon_flag_19: bpy.props.BoolProperty(name="Unknown Flag 19 (Unused?)", default=False)
    toon_flag_20: bpy.props.BoolProperty(name="Unknown Flag 20 (Unused?)", default=False)
    toon_flag_21: bpy.props.BoolProperty(name="Unknown Flag 21 (Unused?)", default=False)
    toon_flag_22: bpy.props.BoolProperty(name="Unknown Flag 22 (Unused?)", default=False)
    toon_flag_23: bpy.props.BoolProperty(name="Unknown Flag 23 (Unused?)", default=False)
    toon_flag_24: bpy.props.BoolProperty(name="Unknown Flag 24 (Unused?)", default=False)
    toon_flag_25: bpy.props.BoolProperty(name="Unknown Flag 25 (Unused?)", default=False)
    toon_flag_26: bpy.props.BoolProperty(name="Unknown Flag 26 (Unused?)", default=False)
    toon_flag_27: bpy.props.BoolProperty(name="Unknown Flag 27 (Unused?)", default=False)
    toon_flag_28: bpy.props.BoolProperty(name="Unknown Flag 28 (Unused?)", default=False)
    toon_flag_29: bpy.props.BoolProperty(name="Unknown Flag 29 (Unused?)", default=False)
    toon_flag_30: bpy.props.BoolProperty(name="Unknown Flag 30 (Unused?)", default=False)
    toon_flag_31: bpy.props.BoolProperty(name="Unknown Flag 31 (Unused?)", default=False)
  
    ####################
    # ATTRIBUTE TYPE 1 #
    ####################
    
    has_a1:  bpy.props.BoolProperty(name="Active")
    
    a1_unknown_0x00:       bpy.props.FloatProperty(name="unknown 0x00", default=0.)
    a1_unknown_0x04:       bpy.props.FloatProperty(name="unknown 0x04", default=0.)
    a1_unknown_0x08:       bpy.props.FloatProperty(name="unknown 0x08", default=0.)
    a1_unknown_0x0C:       bpy.props.FloatProperty(name="unknown 0x0C", default=0.)
    a1_unknown_0x10:       bpy.props.FloatProperty(name="unknown 0x10", default=0.)
    a1_unknown_0x14:       bpy.props.FloatProperty(name="unknown 0x14", default=0.)
    a1_unknown_0x18:       bpy.props.FloatProperty(name="unknown 0x18", default=0.)
    a1_unknown_0x1C:       bpy.props.FloatProperty(name="unknown 0x1C", default=0.)
    a1_unknown_0x20:       bpy.props.FloatProperty(name="unknown 0x20", default=0.)
    a1_unknown_0x24:       bpy.props.FloatProperty(name="unknown 0x24", default=0.)
    a1_unknown_0x28:       bpy.props.FloatProperty(name="unknown 0x28", default=0.)
    a1_unknown_0x2C:       bpy.props.FloatProperty(name="unknown 0x2C", default=0.)
    
    a1_ctr_flag_0:  bpy.props.BoolProperty(name="Unknown Attr. Flag 0",            default=True)
    a1_ctr_flag_1:  bpy.props.BoolProperty(name="Unknown Attr. Flag 1  (Unused?)", default=False)
    a1_ctr_flag_2:  bpy.props.BoolProperty(name="Unknown Attr. Flag 2  (Unused?)", default=False)
    a1_ctr_flag_3:  bpy.props.BoolProperty(name="Unknown Attr. Flag 3  (Unused?)", default=False)
    a1_ctr_flag_4:  bpy.props.BoolProperty(name="Unknown Attr. Flag 4  (Unused?)", default=False)
    a1_ctr_flag_5:  bpy.props.BoolProperty(name="Unknown Attr. Flag 5  (Unused?)", default=False)
    a1_ctr_flag_6:  bpy.props.BoolProperty(name="Unknown Attr. Flag 6  (Unused?)", default=False)
    a1_ctr_flag_7:  bpy.props.BoolProperty(name="Unknown Attr. Flag 7  (Unused?)", default=False)
    a1_ctr_flag_8:  bpy.props.BoolProperty(name="Unknown Attr. Flag 8  (Unused?)", default=False)
    a1_ctr_flag_9:  bpy.props.BoolProperty(name="Unknown Attr. Flag 9  (Unused?)", default=False)
    a1_ctr_flag_10: bpy.props.BoolProperty(name="Unknown Attr. Flag 10 (Unused?)", default=False)
    a1_ctr_flag_11: bpy.props.BoolProperty(name="Unknown Attr. Flag 11 (Unused?)", default=False)
    a1_ctr_flag_12: bpy.props.BoolProperty(name="Unknown Attr. Flag 12 (Unused?)", default=False)
    a1_ctr_flag_13: bpy.props.BoolProperty(name="Unknown Attr. Flag 13 (Unused?)", default=False)
    a1_ctr_flag_14: bpy.props.BoolProperty(name="Unknown Attr. Flag 14 (Unused?)", default=False)
    a1_ctr_flag_15: bpy.props.BoolProperty(name="Unknown Attr. Flag 15 (Unused?)", default=False)
    
    a1_flag_0:  bpy.props.BoolProperty(name="Unknown Flag 0",            default=True)
    a1_flag_1:  bpy.props.BoolProperty(name="Unknown Flag 1",            default=False)
    a1_flag_2:  bpy.props.BoolProperty(name="Unknown Flag 2",            default=False)
    a1_flag_3:  bpy.props.BoolProperty(name="Unknown Flag 3",            default=False)
    a1_flag_4:  bpy.props.BoolProperty(name="Unknown Flag 4",            default=False)
    a1_flag_5:  bpy.props.BoolProperty(name="Unknown Flag 5",            default=False)
    a1_flag_6:  bpy.props.BoolProperty(name="Unknown Flag 6",            default=False)
    a1_flag_7:  bpy.props.BoolProperty(name="Unknown Flag 7",            default=False)
    a1_flag_8:  bpy.props.BoolProperty(name="Unknown Flag 8  (Unused?)", default=False)
    a1_flag_9:  bpy.props.BoolProperty(name="Unknown Flag 9  (Unused?)", default=False)
    a1_flag_10: bpy.props.BoolProperty(name="Unknown Flag 10 (Unused?)", default=False)
    a1_flag_11: bpy.props.BoolProperty(name="Unknown Flag 11 (Unused?)", default=False)
    a1_flag_12: bpy.props.BoolProperty(name="Unknown Flag 12 (Unused?)", default=False)
    a1_flag_13: bpy.props.BoolProperty(name="Unknown Flag 13 (Unused?)", default=False)
    a1_flag_14: bpy.props.BoolProperty(name="Unknown Flag 14 (Unused?)", default=False)
    a1_flag_15: bpy.props.BoolProperty(name="Unknown Flag 15 (Unused?)", default=False)
    a1_flag_16: bpy.props.BoolProperty(name="Unknown Flag 16 (Unused?)", default=False)
    a1_flag_17: bpy.props.BoolProperty(name="Unknown Flag 17 (Unused?)", default=False)
    a1_flag_18: bpy.props.BoolProperty(name="Unknown Flag 18 (Unused?)", default=False)
    a1_flag_19: bpy.props.BoolProperty(name="Unknown Flag 19 (Unused?)", default=False)
    a1_flag_20: bpy.props.BoolProperty(name="Unknown Flag 20 (Unused?)", default=False)
    a1_flag_21: bpy.props.BoolProperty(name="Unknown Flag 21 (Unused?)", default=False)
    a1_flag_22: bpy.props.BoolProperty(name="Unknown Flag 22 (Unused?)", default=False)
    a1_flag_23: bpy.props.BoolProperty(name="Unknown Flag 23 (Unused?)", default=False)
    a1_flag_24: bpy.props.BoolProperty(name="Unknown Flag 24 (Unused?)", default=False)
    a1_flag_25: bpy.props.BoolProperty(name="Unknown Flag 25 (Unused?)", default=False)
    a1_flag_26: bpy.props.BoolProperty(name="Unknown Flag 26 (Unused?)", default=False)
    a1_flag_27: bpy.props.BoolProperty(name="Unknown Flag 27 (Unused?)", default=False)
    a1_flag_28: bpy.props.BoolProperty(name="Unknown Flag 28 (Unused?)", default=False)
    a1_flag_29: bpy.props.BoolProperty(name="Unknown Flag 29 (Unused?)", default=False)
    a1_flag_30: bpy.props.BoolProperty(name="Unknown Flag 30 (Unused?)", default=False)
    a1_flag_31: bpy.props.BoolProperty(name="Unknown Flag 31 (Unused?)", default=False)
    
    #####################
    # OUTLINE ATTRIBUTE #
    #####################
    has_outline:   bpy.props.BoolProperty(name="Active")
    # Should replace outline_type with an enum when all types are known
    # These should also have a max of 2**32 - 1, but blender doesn't offer
    # an unsigned int type
    outline_type:  bpy.props.IntProperty(name="Type",  min=0, max=255, default=0)
    outline_color: bpy.props.IntProperty(name="Color", min=0, max=(2**31) - 1, default=0)
    
    outline_ctr_flag_0:  bpy.props.BoolProperty(name="Unknown Attr. Flag 0",            default=True)
    outline_ctr_flag_1:  bpy.props.BoolProperty(name="Unknown Attr. Flag 1  (Unused?)", default=False)
    outline_ctr_flag_2:  bpy.props.BoolProperty(name="Unknown Attr. Flag 2  (Unused?)", default=False)
    outline_ctr_flag_3:  bpy.props.BoolProperty(name="Unknown Attr. Flag 3  (Unused?)", default=False)
    outline_ctr_flag_4:  bpy.props.BoolProperty(name="Unknown Attr. Flag 4  (Unused?)", default=False)
    outline_ctr_flag_5:  bpy.props.BoolProperty(name="Unknown Attr. Flag 5  (Unused?)", default=False)
    outline_ctr_flag_6:  bpy.props.BoolProperty(name="Unknown Attr. Flag 6  (Unused?)", default=False)
    outline_ctr_flag_7:  bpy.props.BoolProperty(name="Unknown Attr. Flag 7  (Unused?)", default=False)
    outline_ctr_flag_8:  bpy.props.BoolProperty(name="Unknown Attr. Flag 8  (Unused?)", default=False)
    outline_ctr_flag_9:  bpy.props.BoolProperty(name="Unknown Attr. Flag 9  (Unused?)", default=False)
    outline_ctr_flag_10: bpy.props.BoolProperty(name="Unknown Attr. Flag 10 (Unused?)", default=False)
    outline_ctr_flag_11: bpy.props.BoolProperty(name="Unknown Attr. Flag 11 (Unused?)", default=False)
    outline_ctr_flag_12: bpy.props.BoolProperty(name="Unknown Attr. Flag 12 (Unused?)", default=False)
    outline_ctr_flag_13: bpy.props.BoolProperty(name="Unknown Attr. Flag 13 (Unused?)", default=False)
    outline_ctr_flag_14: bpy.props.BoolProperty(name="Unknown Attr. Flag 14 (Unused?)", default=False)
    outline_ctr_flag_15: bpy.props.BoolProperty(name="Unknown Attr. Flag 15 (Unused?)", default=False)
    
    ####################
    # ATTRIBUTE TYPE 3 #
    ####################
    
    has_a3:  bpy.props.BoolProperty(name="Active")
    
    a3_unknown_0x00:       bpy.props.FloatProperty(name="unknown 0x00", default=100.)
    a3_unknown_0x04:       bpy.props.FloatProperty(name="unknown 0x04", default=100.)
    a3_unknown_0x08:       bpy.props.FloatProperty(name="unknown 0x08", default=60.)
    a3_unknown_0x0C:       bpy.props.FloatProperty(name="unknown 0x0C", default=70.)
    a3_unknown_0x10:       bpy.props.FloatProperty(name="unknown 0x10", default=50.)
    a3_unknown_0x14:       bpy.props.FloatProperty(name="unknown 0x14", default=25.)
    a3_unknown_0x18:       bpy.props.FloatProperty(name="unknown 0x18", default=0.)
    a3_unknown_0x1C:       bpy.props.FloatProperty(name="unknown 0x1C", default=0.)
    a3_unknown_0x20:       bpy.props.FloatProperty(name="unknown 0x20", default=0.)
    a3_unknown_0x24:       bpy.props.FloatProperty(name="unknown 0x24", default=1.)
    a3_unknown_0x28:       bpy.props.FloatProperty(name="unknown 0x28", default=0.)
    a3_unknown_0x2C:       bpy.props.FloatProperty(name="unknown 0x2C", default=2.)
    
    a3_ctr_flag_0:  bpy.props.BoolProperty(name="Unknown Attr. Flag 0",            default=True)
    a3_ctr_flag_1:  bpy.props.BoolProperty(name="Unknown Attr. Flag 1  (Unused?)", default=False)
    a3_ctr_flag_2:  bpy.props.BoolProperty(name="Unknown Attr. Flag 2  (Unused?)", default=False)
    a3_ctr_flag_3:  bpy.props.BoolProperty(name="Unknown Attr. Flag 3  (Unused?)", default=False)
    a3_ctr_flag_4:  bpy.props.BoolProperty(name="Unknown Attr. Flag 4  (Unused?)", default=False)
    a3_ctr_flag_5:  bpy.props.BoolProperty(name="Unknown Attr. Flag 5  (Unused?)", default=False)
    a3_ctr_flag_6:  bpy.props.BoolProperty(name="Unknown Attr. Flag 6  (Unused?)", default=False)
    a3_ctr_flag_7:  bpy.props.BoolProperty(name="Unknown Attr. Flag 7  (Unused?)", default=False)
    a3_ctr_flag_8:  bpy.props.BoolProperty(name="Unknown Attr. Flag 8  (Unused?)", default=False)
    a3_ctr_flag_9:  bpy.props.BoolProperty(name="Unknown Attr. Flag 9  (Unused?)", default=False)
    a3_ctr_flag_10: bpy.props.BoolProperty(name="Unknown Attr. Flag 10 (Unused?)", default=False)
    a3_ctr_flag_11: bpy.props.BoolProperty(name="Unknown Attr. Flag 11 (Unused?)", default=False)
    a3_ctr_flag_12: bpy.props.BoolProperty(name="Unknown Attr. Flag 12 (Unused?)", default=False)
    a3_ctr_flag_13: bpy.props.BoolProperty(name="Unknown Attr. Flag 13 (Unused?)", default=False)
    a3_ctr_flag_14: bpy.props.BoolProperty(name="Unknown Attr. Flag 14 (Unused?)", default=False)
    a3_ctr_flag_15: bpy.props.BoolProperty(name="Unknown Attr. Flag 15 (Unused?)", default=False)
    
    a3_flag_0:  bpy.props.BoolProperty(name="Unknown Flag 0",            default=True)
    a3_flag_1:  bpy.props.BoolProperty(name="Unknown Flag 1",            default=False)
    a3_flag_2:  bpy.props.BoolProperty(name="Unknown Flag 2",            default=False)
    a3_flag_3:  bpy.props.BoolProperty(name="Unknown Flag 3  (Unused?)", default=False)
    a3_flag_4:  bpy.props.BoolProperty(name="Unknown Flag 4  (Unused?)", default=False)
    a3_flag_5:  bpy.props.BoolProperty(name="Unknown Flag 5  (Unused?)", default=False)
    a3_flag_6:  bpy.props.BoolProperty(name="Unknown Flag 6  (Unused?)", default=False)
    a3_flag_7:  bpy.props.BoolProperty(name="Unknown Flag 7  (Unused?)", default=False)
    a3_flag_8:  bpy.props.BoolProperty(name="Unknown Flag 8  (Unused?)", default=False)
    a3_flag_9:  bpy.props.BoolProperty(name="Unknown Flag 9  (Unused?)", default=False)
    a3_flag_10: bpy.props.BoolProperty(name="Unknown Flag 10 (Unused?)", default=False)
    a3_flag_11: bpy.props.BoolProperty(name="Unknown Flag 11 (Unused?)", default=False)
    a3_flag_12: bpy.props.BoolProperty(name="Unknown Flag 12 (Unused?)", default=False)
    a3_flag_13: bpy.props.BoolProperty(name="Unknown Flag 13 (Unused?)", default=False)
    a3_flag_14: bpy.props.BoolProperty(name="Unknown Flag 14 (Unused?)", default=False)
    a3_flag_15: bpy.props.BoolProperty(name="Unknown Flag 15 (Unused?)", default=False)
    a3_flag_16: bpy.props.BoolProperty(name="Unknown Flag 16 (Unused?)", default=False)
    a3_flag_17: bpy.props.BoolProperty(name="Unknown Flag 17 (Unused?)", default=False)
    a3_flag_18: bpy.props.BoolProperty(name="Unknown Flag 18 (Unused?)", default=False)
    a3_flag_19: bpy.props.BoolProperty(name="Unknown Flag 19 (Unused?)", default=False)
    a3_flag_20: bpy.props.BoolProperty(name="Unknown Flag 20 (Unused?)", default=False)
    a3_flag_21: bpy.props.BoolProperty(name="Unknown Flag 21 (Unused?)", default=False)
    a3_flag_22: bpy.props.BoolProperty(name="Unknown Flag 22 (Unused?)", default=False)
    a3_flag_23: bpy.props.BoolProperty(name="Unknown Flag 23 (Unused?)", default=False)
    a3_flag_24: bpy.props.BoolProperty(name="Unknown Flag 24 (Unused?)", default=False)
    a3_flag_25: bpy.props.BoolProperty(name="Unknown Flag 25 (Unused?)", default=False)
    a3_flag_26: bpy.props.BoolProperty(name="Unknown Flag 26 (Unused?)", default=False)
    a3_flag_27: bpy.props.BoolProperty(name="Unknown Flag 27 (Unused?)", default=False)
    a3_flag_28: bpy.props.BoolProperty(name="Unknown Flag 28 (Unused?)", default=False)
    a3_flag_29: bpy.props.BoolProperty(name="Unknown Flag 29 (Unused?)", default=False)
    a3_flag_30: bpy.props.BoolProperty(name="Unknown Flag 30 (Unused?)", default=False)
    a3_flag_31: bpy.props.BoolProperty(name="Unknown Flag 31 (Unused?)", default=False)
    
    ####################
    # ATTRIBUTE TYPE 4 #
    ####################
    
    has_a4:  bpy.props.BoolProperty(name="Active")
    
    a4_unknown_0x00:       bpy.props.FloatProperty(name="unknown 0x00", default=0.)
    a4_unknown_0x04:       bpy.props.FloatProperty(name="unknown 0x04", default=0.)
    a4_unknown_0x08:       bpy.props.FloatProperty(name="unknown 0x08", default=0.)
    a4_unknown_0x0C:       bpy.props.FloatProperty(name="unknown 0x0C", default=0.)
    a4_unknown_0x10:       bpy.props.FloatProperty(name="unknown 0x10", default=0.)
    a4_unknown_0x14:       bpy.props.FloatProperty(name="unknown 0x14", default=0.)
    a4_unknown_0x18:       bpy.props.FloatProperty(name="unknown 0x18", default=0.)
    a4_unknown_0x1C:       bpy.props.FloatProperty(name="unknown 0x1C", default=0.)
    a4_unknown_0x20:       bpy.props.FloatProperty(name="unknown 0x20", default=0.)
    a4_unknown_0x24:       bpy.props.FloatProperty(name="unknown 0x24", default=0.)
    a4_unknown_0x28:       bpy.props.FloatProperty(name="unknown 0x28", default=0.)
    a4_unknown_0x2C:       bpy.props.FloatProperty(name="unknown 0x2C", default=0.)
    a4_unknown_0x30:       bpy.props.FloatProperty(name="unknown 0x30", default=0.)
    a4_unknown_0x34:       bpy.props.FloatProperty(name="unknown 0x34", default=0.)
    a4_unknown_0x38:       bpy.props.FloatProperty(name="unknown 0x38", default=1.)
    a4_unknown_0x3C:       bpy.props.FloatProperty(name="unknown 0x3C", default=0.)
    a4_unknown_0x40:       bpy.props.FloatProperty(name="unknown 0x40", default=0.)
    a4_unknown_0x44:       bpy.props.IntProperty(name="unknown 0x44", min=0, max=255, default=1)
    a4_unknown_0x45:       bpy.props.FloatProperty(name="unknown 0x45", default=0.)
    a4_unknown_0x49:       bpy.props.FloatProperty(name="unknown 0x49", default=0.)
    
    a4_ctr_flag_0:  bpy.props.BoolProperty(name="Unknown Attr. Flag 0",            default=True)
    a4_ctr_flag_1:  bpy.props.BoolProperty(name="Unknown Attr. Flag 1  (Unused?)", default=False)
    a4_ctr_flag_2:  bpy.props.BoolProperty(name="Unknown Attr. Flag 2  (Unused?)", default=False)
    a4_ctr_flag_3:  bpy.props.BoolProperty(name="Unknown Attr. Flag 3  (Unused?)", default=False)
    a4_ctr_flag_4:  bpy.props.BoolProperty(name="Unknown Attr. Flag 4  (Unused?)", default=False)
    a4_ctr_flag_5:  bpy.props.BoolProperty(name="Unknown Attr. Flag 5  (Unused?)", default=False)
    a4_ctr_flag_6:  bpy.props.BoolProperty(name="Unknown Attr. Flag 6  (Unused?)", default=False)
    a4_ctr_flag_7:  bpy.props.BoolProperty(name="Unknown Attr. Flag 7  (Unused?)", default=False)
    a4_ctr_flag_8:  bpy.props.BoolProperty(name="Unknown Attr. Flag 8  (Unused?)", default=False)
    a4_ctr_flag_9:  bpy.props.BoolProperty(name="Unknown Attr. Flag 9  (Unused?)", default=False)
    a4_ctr_flag_10: bpy.props.BoolProperty(name="Unknown Attr. Flag 10 (Unused?)", default=False)
    a4_ctr_flag_11: bpy.props.BoolProperty(name="Unknown Attr. Flag 11 (Unused?)", default=False)
    a4_ctr_flag_12: bpy.props.BoolProperty(name="Unknown Attr. Flag 12 (Unused?)", default=False)
    a4_ctr_flag_13: bpy.props.BoolProperty(name="Unknown Attr. Flag 13 (Unused?)", default=False)
    a4_ctr_flag_14: bpy.props.BoolProperty(name="Unknown Attr. Flag 14 (Unused?)", default=False)
    a4_ctr_flag_15: bpy.props.BoolProperty(name="Unknown Attr. Flag 15 (Unused?)", default=False)
    
    a4_flag_0:  bpy.props.BoolProperty(name="Unknown Flag 0",            default=True)
    a4_flag_1:  bpy.props.BoolProperty(name="Unknown Flag 1",            default=False)
    a4_flag_2:  bpy.props.BoolProperty(name="Unknown Flag 2",            default=False)
    a4_flag_3:  bpy.props.BoolProperty(name="Unknown Flag 3",            default=False)
    a4_flag_4:  bpy.props.BoolProperty(name="Unknown Flag 4",            default=False)
    a4_flag_5:  bpy.props.BoolProperty(name="Unknown Flag 5",            default=False)
    a4_flag_6:  bpy.props.BoolProperty(name="Unknown Flag 6",            default=False)
    a4_flag_7:  bpy.props.BoolProperty(name="Unknown Flag 7",            default=False)
    a4_flag_8:  bpy.props.BoolProperty(name="Unknown Flag 8  (Unused?)", default=False)
    a4_flag_9:  bpy.props.BoolProperty(name="Unknown Flag 9  (Unused?)", default=False)
    a4_flag_10: bpy.props.BoolProperty(name="Unknown Flag 10 (Unused?)", default=False)
    a4_flag_11: bpy.props.BoolProperty(name="Unknown Flag 11 (Unused?)", default=False)
    a4_flag_12: bpy.props.BoolProperty(name="Unknown Flag 12 (Unused?)", default=False)
    a4_flag_13: bpy.props.BoolProperty(name="Unknown Flag 13 (Unused?)", default=False)
    a4_flag_14: bpy.props.BoolProperty(name="Unknown Flag 14 (Unused?)", default=False)
    a4_flag_15: bpy.props.BoolProperty(name="Unknown Flag 15 (Unused?)", default=False)
    a4_flag_16: bpy.props.BoolProperty(name="Unknown Flag 16 (Unused?)", default=False)
    a4_flag_17: bpy.props.BoolProperty(name="Unknown Flag 17 (Unused?)", default=False)
    a4_flag_18: bpy.props.BoolProperty(name="Unknown Flag 18 (Unused?)", default=False)
    a4_flag_19: bpy.props.BoolProperty(name="Unknown Flag 19 (Unused?)", default=False)
    a4_flag_20: bpy.props.BoolProperty(name="Unknown Flag 20 (Unused?)", default=False)
    a4_flag_21: bpy.props.BoolProperty(name="Unknown Flag 21 (Unused?)", default=False)
    a4_flag_22: bpy.props.BoolProperty(name="Unknown Flag 22 (Unused?)", default=False)
    a4_flag_23: bpy.props.BoolProperty(name="Unknown Flag 23 (Unused?)", default=False)
    a4_flag_24: bpy.props.BoolProperty(name="Unknown Flag 24 (Unused?)", default=False)
    a4_flag_25: bpy.props.BoolProperty(name="Unknown Flag 25 (Unused?)", default=False)
    a4_flag_26: bpy.props.BoolProperty(name="Unknown Flag 26 (Unused?)", default=False)
    a4_flag_27: bpy.props.BoolProperty(name="Unknown Flag 27 (Unused?)", default=False)
    a4_flag_28: bpy.props.BoolProperty(name="Unknown Flag 28 (Unused?)", default=False)
    a4_flag_29: bpy.props.BoolProperty(name="Unknown Flag 29 (Unused?)", default=False)
    a4_flag_30: bpy.props.BoolProperty(name="Unknown Flag 30 (Unused?)", default=False)
    a4_flag_31: bpy.props.BoolProperty(name="Unknown Flag 31 (Unused?)", default=False)
    
    ####################
    # ATTRIBUTE TYPE 5 #
    ####################
    
    has_a5:  bpy.props.BoolProperty(name="Active")
    
    a5_unknown_0x00:       bpy.props.IntProperty(name="unknown 0x00")
    a5_unknown_0x04:       bpy.props.IntProperty(name="unknown 0x04")
    a5_unknown_0x08:       bpy.props.FloatProperty(name="unknown 0x08")
    a5_unknown_0x0C:       bpy.props.FloatProperty(name="unknown 0x0C")
    a5_unknown_0x10:       bpy.props.FloatProperty(name="unknown 0x10")
    a5_unknown_0x14:       bpy.props.FloatProperty(name="unknown 0x14")
    a5_unknown_0x18:       bpy.props.FloatProperty(name="unknown 0x18")
    a5_unknown_0x1C:       bpy.props.FloatProperty(name="unknown 0x1C")
    a5_unknown_0x20:       bpy.props.FloatProperty(name="unknown 0x20")
    a5_unknown_0x24:       bpy.props.FloatProperty(name="unknown 0x24")
    a5_unknown_0x28:       bpy.props.FloatProperty(name="unknown 0x28")
    a5_unknown_0x2C:       bpy.props.FloatProperty(name="unknown 0x2C")
    a5_unknown_0x30:       bpy.props.FloatProperty(name="unknown 0x30")
    
    a5_ctr_flag_0:  bpy.props.BoolProperty(name="Unknown Attr. Flag 0", default=True)
    a5_ctr_flag_1:  bpy.props.BoolProperty(name="Unknown Attr. Flag 1")
    a5_ctr_flag_2:  bpy.props.BoolProperty(name="Unknown Attr. Flag 2")
    a5_ctr_flag_3:  bpy.props.BoolProperty(name="Unknown Attr. Flag 3")
    a5_ctr_flag_4:  bpy.props.BoolProperty(name="Unknown Attr. Flag 4")
    a5_ctr_flag_5:  bpy.props.BoolProperty(name="Unknown Attr. Flag 5")
    a5_ctr_flag_6:  bpy.props.BoolProperty(name="Unknown Attr. Flag 6")
    a5_ctr_flag_7:  bpy.props.BoolProperty(name="Unknown Attr. Flag 7")
    a5_ctr_flag_8:  bpy.props.BoolProperty(name="Unknown Attr. Flag 8")
    a5_ctr_flag_9:  bpy.props.BoolProperty(name="Unknown Attr. Flag 9")
    a5_ctr_flag_10: bpy.props.BoolProperty(name="Unknown Attr. Flag 10")
    a5_ctr_flag_11: bpy.props.BoolProperty(name="Unknown Attr. Flag 11")
    a5_ctr_flag_12: bpy.props.BoolProperty(name="Unknown Attr. Flag 12")
    a5_ctr_flag_13: bpy.props.BoolProperty(name="Unknown Attr. Flag 13")
    a5_ctr_flag_14: bpy.props.BoolProperty(name="Unknown Attr. Flag 14")
    a5_ctr_flag_15: bpy.props.BoolProperty(name="Unknown Attr. Flag 15")
    
    a5_flag_0:  bpy.props.BoolProperty(name="Unknown Flag 0")
    a5_flag_1:  bpy.props.BoolProperty(name="Unknown Flag 1")
    a5_flag_2:  bpy.props.BoolProperty(name="Unknown Flag 2")
    a5_flag_3:  bpy.props.BoolProperty(name="Unknown Flag 3")
    a5_flag_4:  bpy.props.BoolProperty(name="Unknown Flag 4")
    a5_flag_5:  bpy.props.BoolProperty(name="Unknown Flag 5")
    a5_flag_6:  bpy.props.BoolProperty(name="Unknown Flag 6")
    a5_flag_7:  bpy.props.BoolProperty(name="Unknown Flag 7")
    a5_flag_8:  bpy.props.BoolProperty(name="Unknown Flag 8")
    a5_flag_9:  bpy.props.BoolProperty(name="Unknown Flag 9")
    a5_flag_10: bpy.props.BoolProperty(name="Unknown Flag 10")
    a5_flag_11: bpy.props.BoolProperty(name="Unknown Flag 11")
    a5_flag_12: bpy.props.BoolProperty(name="Unknown Flag 12")
    a5_flag_13: bpy.props.BoolProperty(name="Unknown Flag 13")
    a5_flag_14: bpy.props.BoolProperty(name="Unknown Flag 14")
    a5_flag_15: bpy.props.BoolProperty(name="Unknown Flag 15")
    a5_flag_16: bpy.props.BoolProperty(name="Unknown Flag 16")
    a5_flag_17: bpy.props.BoolProperty(name="Unknown Flag 17")
    a5_flag_18: bpy.props.BoolProperty(name="Unknown Flag 18")
    a5_flag_19: bpy.props.BoolProperty(name="Unknown Flag 19")
    a5_flag_20: bpy.props.BoolProperty(name="Unknown Flag 20")
    a5_flag_21: bpy.props.BoolProperty(name="Unknown Flag 21")
    a5_flag_22: bpy.props.BoolProperty(name="Unknown Flag 22")
    a5_flag_23: bpy.props.BoolProperty(name="Unknown Flag 23")
    a5_flag_24: bpy.props.BoolProperty(name="Unknown Flag 24")
    a5_flag_25: bpy.props.BoolProperty(name="Unknown Flag 25")
    a5_flag_26: bpy.props.BoolProperty(name="Unknown Flag 26")
    a5_flag_27: bpy.props.BoolProperty(name="Unknown Flag 27")
    a5_flag_28: bpy.props.BoolProperty(name="Unknown Flag 28")
    a5_flag_29: bpy.props.BoolProperty(name="Unknown Flag 29")
    a5_flag_30: bpy.props.BoolProperty(name="Unknown Flag 30")
    a5_flag_31: bpy.props.BoolProperty(name="Unknown Flag 31")
    
    ####################
    # ATTRIBUTE TYPE 6 #
    ####################
    
    has_a6:  bpy.props.BoolProperty(name="Active")
    
    a6_unknown_0x00:       bpy.props.IntProperty(name="unknown 0x00")
    a6_unknown_0x04:       bpy.props.IntProperty(name="unknown 0x04")
    a6_unknown_0x08:       bpy.props.IntProperty(name="unknown 0x08")
    
    a6_ctr_flag_0:  bpy.props.BoolProperty(name="Unknown Attr. Flag 0", default=True)
    a6_ctr_flag_1:  bpy.props.BoolProperty(name="Unknown Attr. Flag 1")
    a6_ctr_flag_2:  bpy.props.BoolProperty(name="Unknown Attr. Flag 2")
    a6_ctr_flag_3:  bpy.props.BoolProperty(name="Unknown Attr. Flag 3")
    a6_ctr_flag_4:  bpy.props.BoolProperty(name="Unknown Attr. Flag 4")
    a6_ctr_flag_5:  bpy.props.BoolProperty(name="Unknown Attr. Flag 5")
    a6_ctr_flag_6:  bpy.props.BoolProperty(name="Unknown Attr. Flag 6")
    a6_ctr_flag_7:  bpy.props.BoolProperty(name="Unknown Attr. Flag 7")
    a6_ctr_flag_8:  bpy.props.BoolProperty(name="Unknown Attr. Flag 8")
    a6_ctr_flag_9:  bpy.props.BoolProperty(name="Unknown Attr. Flag 9")
    a6_ctr_flag_10: bpy.props.BoolProperty(name="Unknown Attr. Flag 10")
    a6_ctr_flag_11: bpy.props.BoolProperty(name="Unknown Attr. Flag 11")
    a6_ctr_flag_12: bpy.props.BoolProperty(name="Unknown Attr. Flag 12")
    a6_ctr_flag_13: bpy.props.BoolProperty(name="Unknown Attr. Flag 13")
    a6_ctr_flag_14: bpy.props.BoolProperty(name="Unknown Attr. Flag 14")
    a6_ctr_flag_15: bpy.props.BoolProperty(name="Unknown Attr. Flag 15")
    
    ####################
    # ATTRIBUTE TYPE 7 #
    ####################
    
    has_a7:  bpy.props.BoolProperty(name="Active")
    
    a7_ctr_flag_0:  bpy.props.BoolProperty(name="Unknown Attr. Flag 0", default=True)
    a7_ctr_flag_1:  bpy.props.BoolProperty(name="Unknown Attr. Flag 1  (Unused?)", default=False)
    a7_ctr_flag_2:  bpy.props.BoolProperty(name="Unknown Attr. Flag 2  (Unused?)", default=False)
    a7_ctr_flag_3:  bpy.props.BoolProperty(name="Unknown Attr. Flag 3  (Unused?)", default=False)
    a7_ctr_flag_4:  bpy.props.BoolProperty(name="Unknown Attr. Flag 4  (Unused?)", default=False)
    a7_ctr_flag_5:  bpy.props.BoolProperty(name="Unknown Attr. Flag 5  (Unused?)", default=False)
    a7_ctr_flag_6:  bpy.props.BoolProperty(name="Unknown Attr. Flag 6  (Unused?)", default=False)
    a7_ctr_flag_7:  bpy.props.BoolProperty(name="Unknown Attr. Flag 7  (Unused?)", default=False)
    a7_ctr_flag_8:  bpy.props.BoolProperty(name="Unknown Attr. Flag 8  (Unused?)", default=False)
    a7_ctr_flag_9:  bpy.props.BoolProperty(name="Unknown Attr. Flag 9  (Unused?)", default=False)
    a7_ctr_flag_10: bpy.props.BoolProperty(name="Unknown Attr. Flag 10 (Unused?)", default=False)
    a7_ctr_flag_11: bpy.props.BoolProperty(name="Unknown Attr. Flag 11 (Unused?)", default=False)
    a7_ctr_flag_12: bpy.props.BoolProperty(name="Unknown Attr. Flag 12 (Unused?)", default=False)
    a7_ctr_flag_13: bpy.props.BoolProperty(name="Unknown Attr. Flag 13 (Unused?)", default=False)
    a7_ctr_flag_14: bpy.props.BoolProperty(name="Unknown Attr. Flag 14 (Unused?)", default=False)
    a7_ctr_flag_15: bpy.props.BoolProperty(name="Unknown Attr. Flag 15 (Unused?)", default=False)
