import numpy as np
import copy

def gaussianElimination(aMat):  # for square matrix
    """
    One of solution of simultaneous equations.
    @param aMat: N x (N+1). Last column is y figure.
    @return: List of coefficient
    """
    matrix = copy.deepcopy(aMat)
    num_row = len(matrix)  # number of row
    ESP = 0.0000001
    for k in range(num_row):  # forward elimination
        max_column_elem = abs(matrix[k][k])
        ir = k
        if k != num_row:
            for i in range(k+1, num_row):
                ab = abs(matrix[i][k])
                if ab >= max_column_elem:
                    max_column_elem = ab
                    ir = i  # row number of max coefficient
        if max_column_elem < ESP:
            print("Can't resolve")
            return []
        if ir != k:  # swap row
            D = matrix[k]
            matrix[k] = matrix[ir]
            matrix[ir] = D
        for i in range(k+1, num_row):
            alfa = matrix[i][k] / matrix[k][k]  # each element / max element
            for j in range(k, num_row+1):
                matrix[i][j] -= alfa * matrix[k][j]  # subtract same column

    print("Forward", matrix)
    B = np.zeros((num_row, 1))
    for i in range(num_row - 1, -1, -1):  # backward elimination
        T = matrix[i][num_row]  # last column
        for j in range(i + 1, num_row):
            T -= matrix[i][j] * matrix[j][num_row]
        matrix[i][num_row] = T / matrix[i][i]
        B[i][0] = matrix[i][num_row]
    return B