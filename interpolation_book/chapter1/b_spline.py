import numpy as np
import matplotlib.pyplot as plt
import copy

def bSplineBase(aNodeList, i, aDegree, aX):
    """
    @param aNodeList:
    @param i: index of basis function
    @param aDegree: degree + 1
    @param aX: x coordinate
    @return: basis function
    """
    if aDegree == 0:
        if aX < aNodeList[i-1]:
            return 0
        if aX < aNodeList[i]:
            return 1
        return 0
    B1 = bSplineBase(aNodeList, i, aDegree-1, aX)  # recursion
    B2 = bSplineBase(aNodeList, i+1, aDegree-1, aX)  # recursion
    return ((aX - aNodeList[i-1]) * B1 / (aNodeList[i+aDegree-1] - aNodeList[i-1]) +
            (aNodeList[i+aDegree] - aX) * B2 / (aNodeList[i+aDegree] - aNodeList[i]))

def setBSplineBase(aNodeList, aDegree, aX):  # set basic function
    L = []
    for element in aX:
        L.append(bSplineBase(aNodeList, 1, aDegree+1, element))
    return L

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
        print("forward", k)
        print("matrix", matrix)
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

def createNode(aX, aDegree):
    """
    @param aX: x data. x is set at regular intervals. number of data is more than 1.
    @param aDegree:
    @return: node list
    """
    x_num = len(aX)
    nodeList = np.zeros(x_num + aDegree * 2)
    x_interval = aX[1] - aX[0]
    nodeList[aDegree-1] = aX[0] - x_interval
    for i in range(aDegree-2, -1, -1):
        nodeList[i] = nodeList[i+1] - x_interval
    for i in range(x_num):
        nodeList[i+aDegree] = aX[i]
    for i in range(aDegree):
        nodeList[i+x_num+aDegree] = nodeList[i+x_num+aDegree-1] + x_interval
    return nodeList

def createMatrixOfSimultaneousEquations(aNodeList, aDegree, aX_num, aY):
    matrix = np.zeros((aX_num, aX_num+1))
    for i in range(aX_num):
        for j in range(aX_num):
            matrix[i][j] = bSplineBase(aNodeList, j+aDegree, aDegree, aNodeList[i+aDegree])
        matrix[i][aX_num] = aY[i]
    print("b-spline", matrix)
    return matrix

def computeYCoordinate(aCoefficientList, aX_coordinate, aNodeList, aDegree, aDataNum):
    resultArray = []
    for element in aX_coordinate:
        T = 0
        for i in range(aDataNum):
            T += aCoefficientList[i][0] * bSplineBase(aNodeList, i+aDegree, aDegree, element)
        resultArray.append(T)
    return resultArray

def bSplineInterpolation(aX_coordinate, aX_data, aY_data, aDegree):
    x_num = len(aX_data)
    nodeList = createNode(aX_data, aDegree)
    print("node list", nodeList)
    matrix = createMatrixOfSimultaneousEquations(nodeList, aDegree, x_num, aY_data)
    print(matrix)
    coefficientList = gaussianElimination(matrix)
    return computeYCoordinate(coefficientList, aX_coordinate, nodeList, aDegree, x_num)


if __name__ == '__main__':
    """
    nodeList = np.arange(0, 1.2+0.2, 0.2)  # node list
    base_x = np.arange(0, 1.2+0.01, 0.01)  # x for description
    base_y = setBSplineBase(nodeList, 3, base_x)
    plt.plot(base_x, base_y)
    """
    x_data = [1, 2, 3, 4, 5, 6, 7]
    y_data = [3, 5, 4, 6, 4, 7, 9]
    x_coordinate = np.arange(1, 7+0.1, 0.1)
    y_predict = bSplineInterpolation(x_coordinate, x_data, y_data, 3)
    plt.plot(x_coordinate, y_predict)
    plt.grid(True)
    plt.show()
