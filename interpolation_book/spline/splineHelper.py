import numpy as np
import matplotlib.pyplot as plt
from interpolation_book.spline import matrixHelper


def createBSplineBasisFunc(aNodeList, i, aDegree, aX):
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
    B1 = createBSplineBasisFunc(aNodeList, i, aDegree - 1, aX)  # recursion
    B2 = createBSplineBasisFunc(aNodeList, i + 1, aDegree - 1, aX)  # recursion
    return ((aX - aNodeList[i-1]) * B1 / (aNodeList[i+aDegree-1] - aNodeList[i-1]) +
            (aNodeList[i+aDegree] - aX) * B2 / (aNodeList[i+aDegree] - aNodeList[i]))

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

def createMatrixOfSimultaneousEquations(aNodeList, aDegree, aX_data, aY_data):
    x_num = len(aX_data)
    matrix = np.zeros((x_num, x_num+1))
    gap = aDegree // 2
    for i in range(x_num):
        for j in range(x_num):
            matrix[i][j] = createBSplineBasisFunc(aNodeList, j+aDegree-gap, aDegree, aX_data[i])
        matrix[i][x_num] = aY_data[i]
    print("b-spline", matrix)
    return matrix

def computeYCoordinate(aCoefficientList, aX_coordinate, aNodeList, aDegree, aDataNum):
    resultArray = []
    gap = aDegree // 2
    for element in aX_coordinate:
        T = 0
        for i in range(aDataNum):
            T += aCoefficientList[i][0] * createBSplineBasisFunc(aNodeList, i+aDegree-gap, aDegree, element)
        resultArray.append(T)
    return resultArray

def bSplineInterpolation(aX_coordinate, aX_data, aY_data, aDegree):
    x_num = len(aX_data)
    nodeList = createNode(aX_data, aDegree)
    matrix = createMatrixOfSimultaneousEquations(nodeList, aDegree, aX_data, aY_data)
    coefficientList = matrixHelper.gaussianElimination(matrix)
    return computeYCoordinate(coefficientList, aX_coordinate, nodeList, aDegree, x_num)


if __name__ == '__main__':
    x_data = [1, 2, 3, 4, 5, 6, 7, 10]
    y_data = [3, 5, 4, 6, 4, 7, 9, 9]
    x_coordinate = np.arange(1, x_data[-1]+0.1, 0.1)
    y_predict = bSplineInterpolation(x_coordinate, x_data, y_data, 2)
    plt.plot(x_coordinate, y_predict, color="blue")
    plt.scatter(x_data, y_data, color="red")
    plt.grid(True)
    plt.show()
