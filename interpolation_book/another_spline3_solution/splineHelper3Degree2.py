import numpy as np
import matplotlib.pyplot as plt


def BSplineSimpleMethod(aX_data, aY_data, aX_pre):
    """
    Deprecated.
    This method is available ony when x node is regular interval.
    """
    nodeNum = len(aX_data)
    DY = np.zeros(nodeNum)
    for nodeIndex, nodeX in enumerate(aX_data):
        if nodeIndex == 0:  # start
            DY[nodeIndex] = (aY_data[1] - aY_data[0]) / (aX_data[1] - aX_data[0])
        elif nodeIndex == nodeNum-1:  # end
            DY[nodeIndex] = (aY_data[nodeNum-1] - aY_data[nodeNum-2]) / (aX_data[nodeNum-1] - aX_data[nodeNum-2])
        else:
            DY[nodeIndex] = (aY_data[nodeIndex+1] - aY_data[nodeIndex-1]) / (aX_data[nodeIndex+1] - aX_data[nodeIndex-1])  # differential

    Y_pre = np.zeros_like(aX_pre)
    for k in range(nodeNum-1):
        DX = aX_data[k+1] - aX_data[k]
        DX2 = DX * DX
        DX3 = DX * DX * DX
        A1 = 2 * (aY_data[k]-aY_data[k+1]) / DX3 + (DY[k]+DY[k+1]) / DX2
        A2 = 3 * (aY_data[k+1]-aY_data[k]) / DX2 - (2*DY[k]+DY[k+1]) / DX
        A3 = DY[k]
        A4 = aY_data[k]
        for preIndex, preX in enumerate(aX_pre):
            if preX >= aX_data[k] and preX <= aX_data[k + 1]:
                gap = preX - aX_data[k]
                Y_pre[preIndex] = A1 * np.power(gap, 3) + A2 * np.power(gap, 2) + A3 * gap + A4
    Y_pre[-1] = aY_data[nodeNum - 1]
    return Y_pre


if __name__ == '__main__':
    x_data = np.array([1, 2, 3, 4, 5, 6])  # more than 3 data
    y_data = np.array([3, 5, 4, 6, 4, 8])  # more than 3 data
    preInterval = 0.1
    x_predict = np.arange(1, x_data[-1]+0.1, preInterval)
    y_predict = BSplineSimpleMethod(x_data, y_data, x_predict)
    plt.plot(x_predict, y_predict, color="blue")
    plt.grid(True)
    plt.show()
