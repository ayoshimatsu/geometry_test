import numpy as np
import matplotlib.pyplot as plt

"""
毎回基底関数を計算しない方法. Use continuity. Differential is equal at each data point.
Only for 3 degree spline.
Calculation is fast, but solution is different depending on degree. 
"""

def createTable(aX_data, aY_data, DY1, DYN):  # ■ 表の生成
    """
    Resolve simultaneous equations with continuity of spline formula
    Table_k: P_k
    aY_data: Y

    Formula of spline:
    S_k(x) = a_k0 + a_k1(x-x_k) + a_k2(x-x_k)^2 + a_k3(x-x_k)^3

    Coefficient:
    a_k0 = Y_k
    a_k2 = P_k / 2
    a_k3 = (P_k+1 - P_k) / 6 * (x_k+1 - x_k)
    a_k1 = (Y_k+1 - Y_k) / (x_k+1 - x_k) - (x_k+1 - x_k) * ((2 * P_k + P_k+1) / 6)
    """
    numX = len(aX_data)
    intervals = np.zeros(numX)
    doubleIntervals = np.zeros(numX)  # doubleIntervals[1] = 2 * (interval[0] + interval[1])
    Table = np.zeros(numX)
    for i in range(numX - 1):  # intervals[N] = 0
        intervals[i] = aX_data[i+1] - aX_data[i]
    for i in range(1, numX - 1):  # doubleIntervals[0] = 0, doubleIntervals[N] = 0
        doubleIntervals[i] = 2 * (intervals[i] + intervals[i - 1])

    U = (aY_data[1] - aY_data[0]) / intervals[0]  # (f(x_1) - f(x_0)) / dx_0
    for i in range(1, numX-1):
        T = (aY_data[i+1] - aY_data[i]) / intervals[i]  # (f(x_k+1) - f(x_k)) / dx_k
        Table[i] = T - U  # (f(x_k+1) - f(x_k)) / dx_k - (f(x_k) - f(x_k-1)) / dx_k-1
        U = T

    Table[0] = DY1 / 6  # (f(x_1) - f(x_0)) / dx_0 / 6
    Table[numX - 1] = DYN / 6  # (f(x_n) - f(x_n-1)) / dx_n-1 / 6

    """
    Table[0] = (f(x_1) - f(x_0)) / dx_0 / 6
    Table[N-1] = (f(x_n) - f(x_n-1)) / dx_n-1 / 6
    Table[1] = (f(x_2) - f(x_1)) / dx_1 - dx_0 * Table[0]
    Table[N-2] = (f(x_n-1) - f(x_n-2)) / dx_n-2 - (f(x_n-2) - f(x_n-3)) / dx_n-3 - dx_n-2 * Table[n-1]
    """
    Table[1] = Table[1] - intervals[0] * Table[0]  # (f(x_2) - f(x_1)) / dx_1 - (f(x_1) - f(x_0)) / 6
    # (f(x_n-1) - f(x_n-2)) / dx_n-2 - (f(x_n-2) - f(x_n-3)) / dx_n-3 - ((f(x_n) - f(x_n-1)) / dx_n-1 / 6) * dx_n-2
    Table[numX-2] = Table[numX-2] - intervals[numX-2] * Table[numX-1]

    # doubleIntervals[1] = 2 * (interval[0] + interval[1])
    for i in range(1, numX-2):
        ii = i + 1
        T = intervals[i] / doubleIntervals[i]  # dx_i / (2 * (dx_i-1 + dx_i))
        # Table[2] = (f(x_3) - f(x_2)) / dx_2 - (f(x_2) - f(x_1)) / dx_1 - Table[1] * dx_1 / (2 * (dx_0+dx_1))
        Table[ii] -= Table[i] * T
        # (2 * (dx_1 + dx_2)) - dx_1 * (dx_1 / (2 * (dx_o + dx_1)))
        doubleIntervals[ii] -= intervals[i] * T
    for i in range(numX - 2, 0, -1):
        Table[i] = (Table[i] - intervals[i] * Table[i+1]) / doubleIntervals[i]
    Table = 6 * Table  # T: numpy array
    return Table

def Fval(X):
    return (X*X-1) * X  # ■ F値

def unitInt(XN, X, Y, Table):  # 単一補間
    N = len(X)
    i = 0
    j = N-1
    while i < j:  # 補間する区間を見つける
        K = int((i + j) / 2)  # 中央値が
        if X[K] < XN:
            i = K+1  # 小さければ中央+1をiとする
        else:
            j = K  # 大きければ中央をjとする
    if i > 0:
        i -= 1         # iを差し引く
    H = X[i+1] - X[i]
    T = (XN-X[i]) / H  # 補間計算
    return T*Y[i+1] + (1-T)*Y[i] + H*H * (Fval(T) * Table[i+1] + Fval(1-T) * Table[i])

def interp(X, Y, Table):  # 補間
    N = len(X)
    NN = (N-1)*10+1
    XX = np.zeros(NN)
    YY = np.zeros(NN)
    XN = X[0]
    for i in range(NN):
        XX[i] = XN
        YY[i] = unitInt(XN, X, Y, Table)
        print("YY: ", XX[i], YY[i])
        XN += 0.1
    return [XX, YY]

def calculateCoefficient(aX_data, aY_data, aTable):
    """
    Formula of 3 degree spline.
    P_k = aTable[k]
    S_k(x) = a_k0 + a_k1(x-x_k) + a_k2(x-x_k)^2 + a_k3(x-x_k)^3
    Coefficient:
    a_k0 = Y_k
    a_k1 = (Y_k+1 - Y_k) / (x_k+1 - x_k) - (x_k+1 - x_k) * ((2 * P_k + P_k+1) / 6)
    a_k2 = P_k / 2
    a_k3 = (P_k+1 - P_k) / 6 * (x_k+1 - x_k)
    """
    nodeNum = len(aX_data) # number of area between data node
    coefficient = np.zeros((nodeNum, 4))
    for index in range(nodeNum):
        if index == nodeNum-1:
            coefficient[index][0] = aY_data[index]
            coefficient[index][1] = 0
            coefficient[index][2] = 0
            coefficient[index][3] = 0
            continue
        coefficient[index][0] = aY_data[index]
        coefficient[index][1] = (aY_data[index+1]-aY_data[index]) / (aX_data[index+1]-aX_data[index]) \
                                - (aX_data[index+1]-aX_data[index]) * (2*aTable[index]+aTable[index+1]) / 6
        coefficient[index][2] = aTable[index] / 2
        coefficient[index][3] = (aTable[index+1]-aTable[index]) / (6 * (aX_data[index+1]-aX_data[index]))
    return coefficient

def doInterpolation(aCo, aGap):  # aGap: aX_pre-aX_data
    y = aCo[0] + aCo[1]*aGap + aCo[2]*np.power(aGap, 2) + aCo[3]*np.power(aGap, 3)
    return y

def interpolateEveryPoint(aX_data, aY_data, aCoefficient, aX_pre, aThreshold):
    preY = np.zeros_like(aX_pre)
    for preIndex, preX in enumerate(aX_pre):
        for nodeIndex, nodeX in enumerate(aX_data):
            if nodeIndex == 0:
                continue
            if preX >= nodeX - aThreshold and preX <= nodeX + aThreshold:
                preY[preIndex] = aY_data[nodeIndex]
                continue
            if (aX_data[nodeIndex-1] <= preX) and (aX_data[nodeIndex] >= preX):
                preY[preIndex] = doInterpolation(aCoefficient[nodeIndex-1], preX - aX_data[nodeIndex-1])
                continue
    return preY


def BSplineInterpo2(X, Y, aX_pre, aThreshold):
    # Calculate P_k list
    Table = createTable(X, Y, (Y[1]-Y[0])/(X[1]-X[0]), (Y[-1]-Y[-2])/(X[-1]-X[-2]))
    coefficient = calculateCoefficient(X, Y, Table)
    y_pre = interpolateEveryPoint(X, Y, coefficient, aX_pre, aThreshold)
    print(Table)
    print(coefficient)
    print(y_pre)
    #return interp(X, Y, Table)
    return y_pre


if __name__ == '__main__':
    x_data = np.array([1, 2, 3, 4, 5, 8])  # more than 3 data
    y_data = np.array([3, 5, 4, 6, 4, 9])  # more than 3 data
    preInterval = 0.1
    x_predict = np.arange(1, x_data[-1]+0.1, preInterval)
    y_predict = BSplineInterpo2(x_data, y_data, x_predict, preInterval/100)
    plt.plot(x_predict, y_predict, color="blue")
    plt.grid(True)
    plt.show()
