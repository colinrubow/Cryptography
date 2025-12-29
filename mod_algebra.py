from math import gcd


def det(m: list[list[int]]) -> int:
    """
    calculates the determinant of a matrix mod 26

    Arguments
    ---------
    m: the matrix

    Returns
    -------
    the determinant
    """
    n = len(m)
    if n == 1:
        return m[0][0] % 26
    if n == 2:
        return (m[0][0] * m[1][1] - m[0][1] * m[1][0]) % 26

    determinant = 0
    for c in range(n):
        submatrix = [row[:c] + row[c+1:] for row in m[1:]]
        sign = (-1) ** c
        determinant += sign * m[0][c] * det(submatrix)

    return determinant % 26

def adjoint(m: list[list[int]]) -> list[list[int]]:
    """
    calculates the adjoint of a matrix mod 26

    Arguments
    ---------
    m: the matrix

    Returns
    -------
    the adjoint matrix
    """
    n = len(m)
    if n == 1:
        return [[1]]

    adj = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for k, row in enumerate(m) if k != i]
            sign = (-1) ** (i + j)
            adj[j][i] = (sign * det(submatrix)) % 26

    return adj

def inv(m: list[list[int]]) -> list[list[int]]:
    """
    calculates the invers of the matrix mod 26

    Arguments
    ---------
    m: the matrix

    Returns
    -------
    the inverse
    """
    # test if invertible
    det_m = det(m)
    if det_m == 0 or gcd(det_m, 26) != 1:
        raise ValueError("m is non-invertible")

    n = len(m)
    if n == 1:
        return [[pow(m[0][0], -1, 26)]]

    det_inv = pow(det_m, -1, 26)
    if n == 2:
        return [
            [(m[1][1]*det_inv)%26, (-m[0][1]*det_inv)%26],
            [(-m[1][0]*det_inv)%26, (m[0][0]*det_inv)%26]
        ]

    m_adj = adjoint(m)
    return [[(num*det_inv)%26 for num in m_adj[i]] for i in range(len(m_adj))]

def mult(m_1: list[list[int]], m_2: list[list[int]]) -> list[list[int]]:
    """
    performs (m_1@m_2)%26

    Arguments
    ---------
    m_1: the left matrix
    m_2: the right matrix

    Return
    ------
    (m_1@m_2)%26
    """
    rows_m1 = len(m_1)
    cols_m1 = len(m_1[0])
    rows_m2 = len(m_2)
    cols_m2 = len(m_2[0])

    if cols_m1 != rows_m2:
        raise ValueError("Incompatible matrix dimensions for multiplication")

    result = [[0] * cols_m2 for _ in range(rows_m1)]

    for i in range(rows_m1):
        for j in range(cols_m2):
            for k in range(cols_m1):
                result[i][j] += m_1[i][k] * m_2[k][j]
            result[i][j] %= 26

    return result

def sub(m_1: list[list[int]], m_2: list[list[int]]) -> list[list[int]]:
    """
    performs m_1 - m_2

    Arguments
    ---------
    m_1: the left matrix
    m_2: the right matrix

    Return
    ------
    m_1 - m_2
    """
    rows = len(m_1)
    cols = len(m_1[0])

    if rows != len(m_2) or cols != len(m_2[0]):
        raise ValueError("subtraction failed, matrices are different sizes")

    result = [[(m_1[i][j] - m_2[i][j])%26 for j in range(cols)] for i in range(rows)]

    return result

def add(m_1: list[list[int]], m_2: list[list[int]]) -> list[list[int]]:
    """
    performs m_1 + m_2

    Arguments
    ---------
    m_1: the left matrix
    m_2: the right matrix

    Return
    ------
    m_1 + m_2
    """
    rows = len(m_1)
    cols = len(m_1[0])

    if rows != len(m_2) or cols != len(m_2[0]):
        raise ValueError("subtraction failed, matrices are different sizes")

    result = [[(m_1[i][j] + m_2[i][j])%26 for j in range(cols)] for i in range(rows)]

    return result

if __name__ == '__main__':
    k = [[10, 5, 12], [3, 14, 21], [8, 9, 11]]

    assert det(k) == 7

    assert adjoint(k) == [[17, 1, 15], [5, 14, 8], [19, 2, 21]]

    assert inv(k) == [[21, 15, 17], [23, 2, 16], [25, 4, 3]]

    m_1 = [[11, 8], [3, 7]]
    m_2 = [[7, 18], [23, 11]]

    assert mult(m_1, m_2) == [[1, 0], [0, 1]]

    assert sub(m_1, m_2) == [[4, 16], [6, 22]]

    assert add(m_1, m_2) == [[18, 0], [0, 18]]
