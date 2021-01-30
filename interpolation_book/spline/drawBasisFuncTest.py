import numpy as np
import matplotlib.pyplot as plt

from interpolation_book.spline import splineHelper

def drawOneBasisFunc(aDegree, aX_data, aBasisFuncIndex, aAx):
    basisFunc = []
    nodeList = splineHelper.createNode(aX_data, aDegree)
    x_coordinate = np.arange(nodeList[0], nodeList[-1]+0.1, 0.1)
    for x in x_coordinate:
        basisFunc.append(splineHelper.bSplineBase(nodeList, aBasisFuncIndex, aDegree, x))
    aAx.plot(x_coordinate, basisFunc, c="blue")
    aAx.scatter(nodeList[aBasisFuncIndex], 0, c='red')
    aAx.vlines(x=aX_data[0], ymin=0, ymax=0.5, linestyles='dashed', colors="black")
    aAx.vlines(x=aX_data[-1], ymin=0, ymax=0.5, linestyles='dashed', colors="black")
    aAx.grid(True)

def drawAllBasisFunc(aDegree, aX_data, aAx):
    nodeList = splineHelper.createNode(aX_data, aDegree)
    x_coordinate = np.arange(nodeList[0], nodeList[-1]+0.1, 0.1)

    for nodeIndex, node in enumerate(nodeList):
        if (nodeIndex == 0):
            continue
        if (node > aX_data[-1]):
            break

        basisFunc = []
        for x in x_coordinate:
            basisFunc.append(splineHelper.bSplineBase(nodeList, nodeIndex, aDegree, x))
        aAx.plot(x_coordinate, basisFunc, c="blue")

    aAx.vlines(x=aX_data[0], ymin=0, ymax=0.5, linestyles='dashed', colors="black")
    aAx.vlines(x=aX_data[-1], ymin=0, ymax=0.5, linestyles='dashed', colors="black")
    aAx.grid(True)

def drawNecessaryBasisFunc(aDegree, aX_data, aX_target, aAx):
    nodeList = splineHelper.createNode(aX_data, aDegree)
    x_coordinate = np.arange(nodeList[0], nodeList[-1]+0.1, 0.1)

    for nodeIndex, node in enumerate(nodeList):
        if nodeIndex == 0:
            continue
        if node > aX_data[-1]:
            break

        flag = False
        basisFuncList = []

        if splineHelper.bSplineBase(nodeList, nodeIndex, aDegree, aX_target) > 0:
            print("!!!!!")
            flag = True

        for x in x_coordinate:
            basisFunc = splineHelper.bSplineBase(nodeList, nodeIndex, aDegree, x)
            basisFuncList.append(basisFunc)

        if flag:
            aAx.plot(x_coordinate, basisFuncList, c="red")
        else:
            aAx.plot(x_coordinate, basisFuncList, c="blue")

    aAx.scatter(aX_target, 0, c='orange')
    aAx.vlines(x=aX_data[0], ymin=0, ymax=0.5, linestyles='dashed', colors="black")
    aAx.vlines(x=aX_data[-1], ymin=0, ymax=0.5, linestyles='dashed', colors="black")
    aAx.grid(True)


if __name__ == '__main__':
    degree = 6
    x_data = [1, 2, 3, 4, 5, 6, 7]
    y_data = [3, 5, 4, 6, 4, 7, 9]
    x_predict = np.arange(1, 7 + 0.1, 0.1)
    fig = plt.figure()
    ax1 = fig.add_subplot(3, 1, 1)
    ax2 = fig.add_subplot(3, 1, 2)
    ax3 = fig.add_subplot(3, 1, 3)

    drawOneBasisFunc(degree, x_data, degree, ax1)
    drawAllBasisFunc(degree, x_data, ax2)
    drawNecessaryBasisFunc(degree, x_data, x_data[0], ax3)

    plt.show()
