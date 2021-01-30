import numpy as np

def array_func(aNum1: int, aNum2: int):
    if aNum2 != 0:
        return [[0 for _ in range(aNum2)] for _ in range(aNum1)]
    return [0 for _ in range(aNum1)]

def copyArray(aArray):
    num1 = len(aArray)
    num2 = len(aArray[0])
    copy = array_func(num1, num2)
    for i in range(num1):
        for j in range(num2):
            copy[i][j] = aArray[i][j]
    return copy

def gaussianElimination(aMat):  # for square matrix
    matrix = copyArray(aMat)
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
    B = array_func(num_row, 1)  # create empty one array for result matrix
    for i in range(num_row - 1, -1, -1):  # backward elimination
        T = matrix[i][num_row]  # last column
        for j in range(i + 1, num_row):
            T -= matrix[i][j] * matrix[j][num_row]
        matrix[i][num_row] = T / matrix[i][i]
        B[i][0] = matrix[i][num_row]
    return B

def setParam(XT, YT):
    """
    Create matrix for gaussian elimination and execute gaussian elimination.
    @param XT: insert parameter
    @type XT: one array
    @param YT: output
    @type YT: one array
    @return:
    @rtype:
    """
    N = len(XT)
    N1 = N + 1
    A = array_func(N, N1)
    for i in range(N):
        X = XT[i]
        A[i][0] = 1
        for j in range(1, N):
            A[i][j] = A[i][j - 1] * X
        A[i][N] = YT[i]
    print(A)
    return gaussianElimination(A)

def Interpolate(X, Param):
    N = len(Param)
    XX = 1
    T = 0
    for i in range(N):
        T += XX * Param[i][0]
        XX *= X
    return T


if __name__ == '__main__':
    """
    0 : 0.0
    10 : 0.17365
    20 : 0.34202
    30 : 0.5
    40 : 0.64279
    f(x) = a0 + a1 * x^1 + a2 * x^2 + a3 * x^3 + ...
    """
    XT = [0, 10, 20, 30, 40]
    YT = [0, 0.17365, 0.34202, 0.5, 0.64279]
    Param = setParam(XT, YT)
    print("係数リスト", Param)
    print("補間結果", Interpolate(22, Param))
