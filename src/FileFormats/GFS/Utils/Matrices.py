def transforms_to_matrix(loc, quat, scale):
	# Quaternion
	q_x = quat[0];
	q_y = quat[1];
	q_z = quat[2];
	q_w = quat[3];

	# Location
	l_x = loc[0];
	l_y = loc[1];
	l_z = loc[2];

	# Scale
	s_x = scale[0];
	s_y = scale[1];
	s_z = scale[2];

	out = [
        0., 0., 0., 0.,
        0., 0., 0., 0.,
        0., 0., 0., 0.
    ]

	# Calculate total transform matrix
	q_xx = q_x * q_x;
	q_yy = q_y * q_y;
	q_zz = q_z * q_z;

	q_xy = q_x * q_y;
	q_xz = q_x * q_z;
	q_yz = q_y * q_z;
	q_xw = q_x * q_w;
	q_yw = q_y * q_w;
	q_zw = q_z * q_w;

	out[0] = 2 * s_x * (0.5 - q_yy - q_zz)
	out[1] = 2 * s_x * (q_xy - q_zw)
	out[2] = 2 * s_x * (q_xz + q_yw)
	out[3] = l_x
	out[4] = 2 * s_y * (q_xy + q_zw)
	out[5] = 2 * s_y * (0.5 - q_xx - q_zz)
	out[6] = 2 * s_y * (q_yz - q_xw)
	out[7] = l_y
	out[8] = 2 * s_z * (q_xz - q_yw)
	out[9] = 2 * s_z * (q_yz + q_xw)
	out[10] = 2 * s_z * (0.5 - q_xx - q_yy)
	out[11] = l_z;

	return out

def multiply_transform_matrices(a, b):
	out = [
        0., 0., 0., 0.,
        0., 0., 0., 0.,
        0., 0., 0., 0.
    ]

	for i in range(0, 12, 4):
		for j in range(4):
			out[i + j] = a[i] * b[j] + a[i + 1] * b[4 + j] + a[i + 2] * b[8 + j]
		out[i + 3] += a[i + 3]

	return out

def multiply_rotation_matrices(a, b):
    out = [
        0., 0., 0.,
        0., 0., 0.,
        0., 0., 0.
    ]

    row_size = 3
    for i in range(0, 9, row_size):
        for j in range(row_size):
            out[i + j] = a[i + 0] * b[0*row_size + j] \
                       + a[i + 1] * b[1*row_size + j] \
                       + a[i + 2] * b[2*row_size + j]

    return out

def are_transform_matrices_close(a, b, rot_tol, trans_tol, debug=False):
    results = [False]*len(a)
    
    # Check if rotations are close
    rot_a = slice_rotation_from_transform(a)
    rot_b = slice_rotation_from_transform(b)
    inv_rot_b = transposed_mat3x3(rot_b)
    
    close_to_identity = multiply_rotation_matrices(rot_a, inv_rot_b)
    close_to_identity[0] -= 1.
    close_to_identity[4] -= 1.
    close_to_identity[8] -= 1.
    
    for i in range(9):
        results[i] = abs(close_to_identity[i]) < rot_tol
    
    # Check if translations are close
    pos_a = slice_translation_from_transform(a)
    pos_b = slice_translation_from_transform(b)
    close_to_zero = [ai - bi for ai, bi in zip(pos_a, pos_b)]
    
    for i in range(3):
        results[i+9] = abs(close_to_zero[i]) < trans_tol
    
    return results

"""
Borrowed from https://github.com/ThomIves/MatrixInverse,
following from this answer https://stackoverflow.com/a/62940942
Errors out if main diagonal is a zero vector?!
"""
def invert_matrix(AM, IM):
    for fd in range(len(AM)):
        fdScaler = 1.0 / AM[fd][fd]
        for j in range(len(AM)):
            AM[fd][j] *= fdScaler
            IM[fd][j] *= fdScaler
        for i in list(range(len(AM)))[0:fd] + list(range(len(AM)))[fd+1:]:
            crScaler = AM[i][fd]
            for j in range(len(AM)):
                AM[i][j] = AM[i][j] - crScaler * AM[fd][j]
                IM[i][j] = IM[i][j] - crScaler * IM[fd][j]
    return IM


def slice_rotation_from_transform(matrix):
    out = [
        0., 0., 0.,
        0., 0., 0.,
        0., 0., 0.,
    ]
    
    out[0]  = matrix[0]
    out[1]  = matrix[1]
    out[2]  = matrix[2]
    out[3]  = matrix[4]
    out[4]  = matrix[5]
    out[5]  = matrix[6]
    out[6]  = matrix[8]
    out[7]  = matrix[9]
    out[8]  = matrix[10]
    
    return out

def slice_translation_from_transform(matrix):
    out = [0., 0., 0.]
    
    out[0]  = matrix[3]
    out[1]  = matrix[7]
    out[2]  = matrix[11]
    
    return out


def transposed_mat3x3(matrix):
    out = [
        0., 0., 0.,
        0., 0., 0.,
        0., 0., 0.,
    ]
    out[0]  = matrix[0]
    out[1]  = matrix[3]
    out[2]  = matrix[6]
    out[3]  = matrix[1]
    out[4]  = matrix[4]
    out[5]  = matrix[7]
    out[6]  = matrix[2]
    out[7]  = matrix[5]
    out[8]  = matrix[8]
    
    return out


def transposed_mat4x4_to_mat4x3(ibpm):
    out = [
        0., 0., 0., 0.,
        0., 0., 0., 0.,
        0., 0., 0., 0.
    ]
    out[0]  = ibpm[0]
    out[1]  = ibpm[4]
    out[2]  = ibpm[8]
    out[3]  = ibpm[12]
    out[4]  = ibpm[1]
    out[5]  = ibpm[5]
    out[6]  = ibpm[9]
    out[7]  = ibpm[13]
    out[8]  = ibpm[2]
    out[9]  = ibpm[6]
    out[10] = ibpm[10]
    out[11] = ibpm[14]
    
    return out

def mat4x3_to_transposed_mat4x4(bpm):
    out = [
        0., 0., 0., 0.,
        0., 0., 0., 0.,
        0., 0., 0., 0.,
        0., 0., 0., 0.
    ]
    
    # Rotation part
    out[0]  = bpm[0]
    out[1]  = bpm[4]
    out[2]  = bpm[8]
    out[4]  = bpm[1]
    out[5]  = bpm[5]
    out[6]  = bpm[9]
    out[8]  = bpm[2]
    out[9]  = bpm[6]
    out[10] = bpm[10]
    
    # Translation part
    out[12] = bpm[3]
    out[13] = bpm[7]
    out[14] = bpm[11]
    
    return out

def invert_pos_rot_matrix(matrix):
    out = [
        0., 0., 0., 0.,
        0., 0., 0., 0.,
        0., 0., 0., 0.
    ]
    
    
    # Transpose rotation part, calculate translations
    out[0]  = matrix[0]
    out[1]  = matrix[4]
    out[2]  = matrix[8]
    out[3]  = -(out[0]*matrix[3] + out[1]*matrix[7] + out[2]*matrix[11])
    out[4]  = matrix[1]
    out[5]  = matrix[5]
    out[6]  = matrix[9]
    out[7]  = -(out[4]*matrix[3] + out[5]*matrix[7] + out[6]*matrix[11])
    out[8]  = matrix[2]
    out[9]  = matrix[6]
    out[10] = matrix[10]
    out[11] = -(out[8]*matrix[3] + out[9]*matrix[7] + out[10]*matrix[11])
    
    return out

def invert_transform_matrix(matrix):
    out = [
        0., 0., 0., 0.,
        0., 0., 0., 0.,
        0., 0., 0., 0.
    ]
    
    # Pos x rot x scale matrices are block matrices:
    # | A B |
    # | C D |
    # Where C is a zero vector and D is 1
    # Use the following result for the inverse of a block matrix:
    # https://math.stackexchange.com/a/4523299
    # Which evaluates to
    # | A^-1  -A^-1*B |
    # |  0       1    |
    
    # First let's invert A
    Ainv = invert_matrix(
        [
            [matrix[0], matrix[1], matrix[2]],
            [matrix[4], matrix[5], matrix[6]],
            [matrix[8], matrix[9], matrix[10]]
        ],
        [
            [1., 0., 0.],
            [0., 1., 0.],
            [0., 0., 1.]
        ]
    )
    
    # Now create the output matrix and calculate the second block
    out[0]  = Ainv[0][0]
    out[1]  = Ainv[0][1]
    out[2]  = Ainv[0][2]
    out[3]  = -(out[0]*matrix[3] + out[1]*matrix[7] + out[2]*matrix[11])
    out[4]  = Ainv[1][0]
    out[5]  = Ainv[1][1]
    out[6]  = Ainv[1][2]
    out[7]  = -(out[4]*matrix[3] + out[5]*matrix[7] + out[6]*matrix[11])
    out[8]  = Ainv[2][0]
    out[9]  = Ainv[2][1]
    out[10] = Ainv[2][2]
    out[11] = -(out[8]*matrix[3] + out[9]*matrix[7] + out[10]*matrix[11])
    
    return out


def normalise_transform_matrix_scale(matrix):
    scale_x = (matrix[0]**2 + matrix[4]**2 + matrix[ 8]**2)**.5
    scale_y = (matrix[1]**2 + matrix[5]**2 + matrix[ 9]**2)**.5
    scale_z = (matrix[2]**2 + matrix[6]**2 + matrix[10]**2)**.5
    
    matrix[0] /= scale_x
    matrix[4] /= scale_x
    matrix[8] /= scale_x
    
    matrix[1] /= scale_y
    matrix[5] /= scale_y
    matrix[9] /= scale_y
    
    matrix[2] /= scale_z
    matrix[6] /= scale_z
    matrix[10] /= scale_z
    
    return matrix
