import math
from pygame import Vector2

# matrix is 2D array


def printMatrix(matrix):
    r = len(matrix)
    if r == 0:
        return
    c = len(matrix[0])

    for i in range(r):
        text = ''
        for j in range(c):
            text += str(matrix[i][j]) + ' '
        print(text)


def determinant(matrix):
    checkMatrix(matrix)

    r = len(matrix)
    c = len(matrix[0])

    if r != c:
        raise Exception('Can\'t find determinant for non-square matrix')

    if r == 1:
        return matrix[0][0]

    det = 0
    for j in range(c):
        mat = []
        for k in range(1, r):
            li = []
            for l in range(c):
                if j == l:
                    continue
                li.append(matrix[k][l])
            mat.append(li)
        if j % 2 == 0:
            det += matrix[0][j] * determinant(mat)
        else:
            det -= matrix[0][j] * determinant(mat)

    return det


def orientation2d(a, b, c):
    matrix = [[a.x, a.y, 1], [b.x, b.y, 1], [c.x, c.y, 1]]
    det = determinant(matrix)
    if det > 0:
        return 1  # anticlockwise
    elif det < 0:
        return -1  # clockwise
    else:
        return 0


def checkMatrix(matrix):
    r = len(matrix)
    if r == 0:
        raise Exception('matrix\'s order is not defined. Row length is zero.')

    c = len(matrix[0])
    if c == 0:
        raise Exception(
            'matrix\'s order is not defined. Column length is zero.')


def multiplication(mat_a, mat_b):
    checkMatrix(mat_a)
    checkMatrix(mat_b)
    r_a = len(mat_a)
    c_a = len(mat_a[0])

    r_b = len(mat_b)
    c_b = len(mat_b[0])

    if c_a != r_b:
        raise Exception(
            'order of column of matrix A does not equal to the order of row of matrix B.')

    result = [[0 for i in range(c_b)] for j in range(r_a)]
    for i in range(r_a):
        for j in range(c_b):
            for k in range(c_a):
                result[i][j] += mat_a[i][k] * mat_b[k][j]

    return result


def minorElement(matrix, i, j):
    r = len(matrix)
    c = len(matrix[0])

    if r != c:
        raise Exception('Can\'t find minor for non-square matrix')

    newMat = []
    for k in range(r):
        if k == i:
            continue

        newRow = []
        for l in range(c):
            if l == j:
                continue
            newRow.append(matrix[k][l])
        newMat.append(newRow)

    return determinant(newMat)


def cofactorElement(matrix, i, j):
    return (1 if (i + j) % 2 == 0 else -1) * minorElement(matrix, i, j)


def tranpose(matrix):
    checkMatrix(matrix)
    r = len(matrix)
    c = len(matrix[0])

    result = [[0 for i in range(r)] for j in range(c)]

    for i in range(r):
        for j in range(c):
            result[j][i] = matrix[i][j]

    return result


def minor(matrix):
    r = len(matrix)
    c = len(matrix[0])

    result = [[0 for i in range(c)] for j in range(r)]
    for i in range(r):
        for j in range(c):
            result[i][j] = minorElement(matrix, i, j)

    return result


def cofactor(matrix):
    r = len(matrix)
    c = len(matrix[0])

    result = [[0 for i in range(c)] for j in range(r)]

    for i in range(r):
        for j in range(c):
            result[i][j] = cofactorElement(matrix, i, j)

    return result


def inverse(matrix):
    checkMatrix(matrix)

    det = determinant(matrix)
    if det == 0:
        raise Exception('determinant of singular matrix can\'t be calculated.')

    det = determinant(matrix)

    result = cofactor(matrix)
    result = tranpose(result)

    r = len(matrix)
    c = len(matrix[0])

    for i in range(r):
        for j in range(c):
            result[i][j] = result[i][j] / det

    return result


def rotateVector(vector, rotation):
    # rotate the vector in anti-clickwise direction
    rad = math.radians(-rotation)
    mat_a = [[math.cos(rad), math.sin(rad)], [-math.sin(rad), math.cos(rad)]]
    mat_v = [[vector.x], [vector.y]]

    res = multiplication(mat_a, mat_v)
    res_vec = Vector2(res[0][0], res[1][0])
    return res_vec


def scaleVector(vector, scale):
    return Vector2(vector.x * scale, vector.y * scale)
