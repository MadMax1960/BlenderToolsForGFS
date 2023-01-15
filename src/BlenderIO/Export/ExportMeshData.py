import array

import bpy
import numpy as np

from ..Utils.ErrorPopup import ReportableException
from ...FileFormats.GFS.SubComponents.CommonStructures.SceneNode.MeshBinary import VertexBinary, VertexAttributes


def export_mesh_data(gfs, armature, pinned_armatures):
    for pinned_armature in pinned_armatures:
        childof_constraints = [constr for constr in pinned_armature.constraints if constr.type == "CHILD_OF"]
        if len(childof_constraints) > 1:
            raise ReportableException(f"Mesh \'{pinned_armature.name}\' must have ONE \'CHILD OF\' constraint.")
        elif len(childof_constraints) == 0:
            return
        
        bone_names = {bn.name: i for i, bn in enumerate(armature.data.bones)}
        constr = childof_constraints[0]
        bone = armature.data.bones[constr.subtarget]
        node_id = bone_names[bone.name]
        
        for mesh_obj in [c for c in pinned_armature.children if c.type == "MESH"]:
            vertices, indices = extract_vertex_data(mesh_obj, bone_names)
            gfs.add_mesh(node_id, vertices, "", [fidx for face in indices for fidx in face], [], 0, 0, 0, False, False)
    

def extract_vertex_data(mesh_obj, bone_names):
    # Switch to input variables
    vweight_floor = 0
    
    mesh = mesh_obj.data
    
    # Deal with any zero vectors
    zero_vec = (0., 0., 0.)
    loop_normals = [l.normal for l in mesh.loops]
    lnorms_zero = [tuple(normal) == zero_vec for normal in loop_normals]
    if any(lnorms_zero):
        if not mesh.has_custom_normals:
            mesh.create_normals_split()
        mesh.calc_normals_split()
        res = []
        for j, iszero in enumerate(lnorms_zero):
            res.append(mesh.loops[j].normal if iszero else loop_normals[j])
        mesh.normals_split_custom_set(res)

    vidx_to_lidxs = generate_vertex_to_loops_map(mesh)
    lidx_to_fidx  = generate_loop_to_face_map(mesh)
    export_verts, export_faces, vgroup_verts = split_verts_by_loop_data(bone_names, mesh_obj, vidx_to_lidxs, lidx_to_fidx, vweight_floor)

    # Remap any groups that were culled in the split...
    old_groups = get_all_nonempty_vertex_groups(mesh_obj)
    for i, group in enumerate(old_groups):
        bone_name = group.name
        bone_id = bone_names[bone_name]
        old_groups[i] = bone_id

    group_map = {old_groups.index(bone_id) : new_idx for new_idx, bone_id in enumerate(vgroup_verts.keys())}
    if export_verts[0].indices is not None:
        for vert in export_verts:
            vert.indices = [group_map[idx] for idx in vert.indices]
    
    return export_verts, export_faces

def generate_vertex_to_loops_map(mesh):
    vidx_to_lidxs = {}
    for loop in mesh.loops:
        if loop.vertex_index not in vidx_to_lidxs:
            vidx_to_lidxs[loop.vertex_index] = []
        vidx_to_lidxs[loop.vertex_index].append(loop.index)
    return vidx_to_lidxs

def generate_loop_to_face_map(mesh):
    lidx_to_fidx = {}
    for face in mesh.polygons:
        for loop_idx in face.loop_indices:
            lidx_to_fidx[loop_idx] = face.index
    return lidx_to_fidx


def split_verts_by_loop_data(bone_names, mesh_obj, vidx_to_lidxs, lidx_to_fidx, vweight_floor):
    mesh = mesh_obj.data
    has_uvs = len(mesh.uv_layers) > 0

    exported_vertices = []
    vgroup_verts = {}
    faces = [{l: mesh.loops[l].vertex_index for l in f.loop_indices} for f in mesh.polygons]
    group_map = {g.index: i for i, g in enumerate(get_all_nonempty_vertex_groups(mesh_obj))}

    map_ids = list(mesh.uv_layers.keys())[:8]
    colour_map = list(mesh.vertex_colors.keys())[:2]
    n_uvs = len(map_ids)
    n_colours = len(colour_map)

    use_normals   = True
    use_tangents  = False
    use_binormals = False
    map_name = map_ids[0] if len(map_ids) else 'dummy'
    can_export_tangents = has_uvs and mesh.uv_layers.get(map_name) is not None and (use_normals and (use_tangents or use_binormals))

    if can_export_tangents:
        mesh.calc_tangents(uvmap=map_name)

    sigfigs = 4
    nloops = len(mesh.loops)

    # Extract normals
    if use_normals:
        normals = [(elem,) for elem in fetch_data(mesh.loops, "normal", sigfigs)]
    else:
        normals = [tuple()]*nloops

    # Extract UVs
    UV_data = [None]*n_uvs
    for i, map_id in enumerate(map_ids):
        UV_data[i] = fetch_data(mesh.uv_layers[map_id].data, "uv", sigfigs+2)
    if len(UV_data):
        UV_data = [tuple(elems) for elems in zip(*UV_data)]
    else:
        UV_data = [tuple()]*nloops

    # Extract colours
    col_data = [None]*n_colours
    for i, map_id in enumerate(colour_map):
        col_data[i] = fetch_data(mesh.vertex_colors[map_id].data, "color", sigfigs)
    if len(col_data):
        col_data = [tuple(elems) for elems in zip(*col_data)]
    else:
        col_data = [tuple()]*nloops

    # Extract tangents
    if can_export_tangents:
        tangents = [(elem,) for elem in fetch_tangent(mesh.loops, sigfigs)]
    else:
        tangents = [tuple()]*nloops

    # Calculate binormals
    if use_binormals and can_export_tangents:
        bitangents = [(tuple(round_to_sigfigs(tangent[0][3] * np.cross(normal, tangent[0][:3]), sigfigs)),) for normal, tangent in zip(normals, tangents)]
    else:
        bitangents = [tuple()]*nloops

    # Make loop -> unique value lookup maps
    loop_idx_to_key = [key for key in (zip(normals, UV_data, col_data, tangents, bitangents))]
    unique_val_map = {key: i for i, key in enumerate(list(set(loop_idx_to_key)))}
    loop_idx_to_unique_key = {i: unique_val_map[key] for i, key in enumerate(loop_idx_to_key)}

    for vert_idx, linked_loops in vidx_to_lidxs.items():
        vertex = mesh.vertices[vert_idx]
        unique_ids = {i: [] for i in list(set(loop_idx_to_unique_key[ll] for ll in linked_loops))}
        for ll in linked_loops:
            unique_ids[loop_idx_to_unique_key[ll]].append(ll)
        unique_values = [(loop_idx_to_key[lids[0]], lids) for id_, lids in unique_ids.items()]

        for unique_value, loops_with_this_value in unique_values:
            group_indices = [grp for grp in vertex.groups if grp.weight > vweight_floor]
            group_bone_ids = [get_bone_id(mesh_obj, bone_names, grp) for grp in group_indices]
            group_weights = [grp.weight for grp in group_indices]


            # Normalise the group weights
            total_weight = sum(group_weights)
            if total_weight > 0.:
                group_weights = [wght / total_weight for wght in group_weights]


            vb = VertexBinary()
            vb.position = vertex.co
            if len(unique_value[0]): vb.normal = unique_value[0][0]
            for attr_idx, value in zip([VertexAttributes.TEXCOORD0,
                                        VertexAttributes.TEXCOORD1,
                                        VertexAttributes.TEXCOORD2,
                                        VertexAttributes.TEXCOORD3,
                                        VertexAttributes.TEXCOORD4,
                                        VertexAttributes.TEXCOORD5,
                                        VertexAttributes.TEXCOORD6,
                                        VertexAttributes.TEXCOORD7], unique_value[1]):
                vb[attr_idx] = value
            if len(unique_value[2]): vb.color1   = unique_value[2][0]
            if len(unique_value[3]): vb.tangent  = unique_value[3][0]
            if len(unique_value[4]): vb.binormal = unique_value[4][0]
            if len(group_indices):
                n_extra = 4 - len(group_indices)
                vb.indices = [*(group_map[grp.group] for grp in group_indices), *([0]*n_extra)]
                vb.weights = [*group_weights, *([0]*n_extra)]

            n_verts = len(exported_vertices)
            exported_vertices.append(vb)

            for l in loops_with_this_value:
                face_idx = lidx_to_fidx[l]
                faces[face_idx][l] = n_verts

            for group_bone_id, weight in zip(group_bone_ids, group_weights):
                if group_bone_id not in vgroup_verts:
                    vgroup_verts[group_bone_id] = []
                vgroup_verts[group_bone_id].append(n_verts)
    faces = [list(face_verts.values()) for face_verts in faces]
    return exported_vertices, faces, vgroup_verts

def get_all_nonempty_vertex_groups(mesh_obj):
    nonempty_vgs = set()
    for vertex in mesh_obj.data.vertices:
        for group in vertex.groups:
            #if group.weight > vweight_floor:
           nonempty_vgs.add(group.group)
    nonempty_vgs = sorted(list(nonempty_vgs))
    nonempty_vgs = [mesh_obj.vertex_groups[idx] for idx in nonempty_vgs]

    return nonempty_vgs


def round_to_sigfigs(x, p):
    """
    Credit to Scott Gigante
    Taken from https://stackoverflow.com/a/59888924
    Rounds a float x to p significant figures
    """
    x = np.asarray(x)
    x_positive = np.where(np.isfinite(x) & (x != 0), np.abs(x), 10**(p-1))
    mags = 10 ** (p - 1 - np.floor(np.log10(x_positive)))
    return np.round(x * mags) / mags


def fetch_data(obj, element, sigfigs):
    dsize = len(getattr(obj[0], element))
    data = array.array('f', [0.0] * (len(obj) * dsize))
    obj.foreach_get(element, data)
    return [tuple(round_to_sigfigs(datum, sigfigs)) for datum in zip(*(iter(data),) * dsize)]


def fetch_tangent(obj, sigfigs):
    dsize = len(getattr(obj[0], "tangent"))
    data = array.array('f', [0.0] * (len(obj) * dsize))
    obj.foreach_get("tangent", data)

    signs = array.array('f', [0.0] * (len(obj)))
    obj.foreach_get("bitangent_sign", data)
    return [(*round_to_sigfigs(datum, sigfigs), sign) for datum, sign in zip(zip(*(iter(data),) * dsize), signs)]

def get_bone_id(mesh_obj, bone_names, grp):
    group_idx = grp.group
    bone_name = mesh_obj.vertex_groups[group_idx].name
    bone_id = bone_names[bone_name]
    return bone_id
