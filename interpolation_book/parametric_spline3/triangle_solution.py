import numpy as np
import matplotlib.pyplot as plt


def TriDiag(A, D):  # 三重対角行列による連立方程式の解法
    """
    A * X = D
    @param A: N x 3
    @param X: N
    @return: R
    """
    N = len(A)
    X = np.zeros(N)
    CC = np.zeros(N)
    btemp = A[0][1]
    X[0] = D[0] / btemp
    for j in range(1, N):  # forward
        CC[j] = A[j-1][2] / btemp
        btemp = A[j][1] - (A[j][0] * CC[j])
        X[j] = (D[j]-A[j][0]*X[j-1]) / btemp
    for j in range(N-2,-1,-1):  # backward
        X[j] -= CC[j+1] * X[j+1]
    return X


def func(P1, P2, P3, Sigma1, Sigma2):
    return 3*((P2-P1)*Sigma2/Sigma1+(P3-P2)*Sigma1/Sigma2)

def clampedConditio(Sigma, N, Point, P1d, Pnd):  # 固定条件
    """
    @param Sigma: interval of s
    @param N: number of sample
    @param Point: X, Y sample coordinate
    @param P1d: differential at start
    @param Pnd: differential at end
    @return: 3 Matrix. List of differential at every sample point.
    """
    A = np.zeros((N, 3))
    Pd = np.zeros((2, N))
    Dd = np.zeros((2, N))
    Dtemp = np.zeros(N)

    A[0][0] = 0  # start boundary condition
    A[0][1] = 2*(Sigma[0]+Sigma[1])  # 端の境界条件
    A[0][2] = Sigma[0]
    A[N-1][0] = Sigma[N-2]
    A[N-1][1] = 2*(Sigma[N-3] + Sigma[N-2])
    A[N-1][2] = 0

    for k in range(1, N-1):  # 端以外の境界条件
        A[k][0] = Sigma[k]
        A[k][1] = 2*(Sigma[k - 1]+Sigma[k])
        A[k][2] = Sigma[k - 1]
    for j in range(2):  # パラメータ設定. X, Y coordinate
        for k in range(1, N-1):
            Dd[j][k-1] = func(Point[k-1][j], Point[k][j],
                              Point[k+1][j], Sigma[k-1], Sigma[k])
        Dd[j][0] = Dd[j][0] - Sigma[1] * P1d[j]
        Dd[j][N-3] = Dd[j][N-3] - Sigma[N-3] * Pnd[j]
        for k in range(N):
            Dtemp[k] = Dd[j][k]
        Ptemp = TriDiag(A, Dtemp)  # 連立方程式を解く
        for k in range(N-1):
            Pd[j][k + 1] = Ptemp[k]
        Pd[j][0] = P1d[j]
        Pd[j][N-1] = Pnd[j]
    return [Pd, Dd, A]

def relaxedCondition(Sigma, N, Point):
    A = np.zeros((N, 3))
    Pd = np.zeros((2, N))  # X and Y differential
    Dd = np.zeros((2, N))  # X and Y right
    Dtemp = np.zeros(N)

    A[0][0] = 0  # start boundary condition
    A[0][1] = 2*Sigma[0]
    A[0][2] = Sigma[0]
    A[N-1][0] = Sigma[N-2]  # end boundary condition
    A[N-1][1] = 2*Sigma[N-2]
    A[N-1][2] = 0
    for k in range(1, N-1):  # boundary condition except edges
        A[k][0] = Sigma[k]
        A[k][1] = 2*(Sigma[k]+Sigma[k-1])
        A[k][2] = Sigma[k-1]
    for j in range(2):  # X and Y
        Dd[j][0] = 3*(Point[1][j]-Point[0][j])  # start
        Dd[j][N-1] = 3*(Point[N-1][j]-Point[N-2][j])  # end
        for k in range(1, N-1):  # calculate of triangle matrix
            Dd[j][k] = func(Point[k - 1][j], Point[k][j],
                            Point[k + 1][j], Sigma[k - 1], Sigma[k])
        for k in range(N):
            Dtemp[k] = Dd[j][k]
        Ptemp = TriDiag(A, Dtemp)  # 連立方程式を解く
        for k in range(N):
            Pd[j][k] = Ptemp[k]
    return [Pd, Dd, A]

def Spline(Point, Sigma, P1d, Pnd, ds, Cond, aAx):  # スプライン曲線
    N = len(Point)
    Ak0 = np.zeros(2)
    Ak1 = np.zeros(2)
    Ak2 = np.zeros(2)
    Ak3 = np.zeros(2)
    if Cond:
        R = clampedConditio(Sigma, N, Point, P1d, Pnd)  # 固定条件
    else:
        R = relaxedCondition(Sigma, N, Point)  # 自然条件
    Pd = R[0]  # differential at sample point

    resultX = []
    resultY = []

    # Move(Point[0][0], Point[0][1])  # 最初の点位置に移動
    for k in range(N-1):  # number of sample data
        for j in range(2):  # X, Y. Set coefficient.
            """
            X = F(s) = a_x * s^3 + b_x * s^2 + c_x * s + d_x 
            Y = G(s) = a_y * s^3 + b_y * s^2 + c_Y * s + d_y 
            sigma: interval of parameter s
            """
            Sigma2 = Sigma[k]*Sigma[k]
            Sigma3 = Sigma[k]*Sigma2
            Ak0[j] = (2*(Point[k][j]-Point[k+1][j])/Sigma3
                      + (Pd[j][k] + Pd[j][k+1])/Sigma2)
            Ak1[j] = (3*(Point[k+1][j]-Point[k][j])/Sigma2
                      - (2*Pd[j][k] + Pd[j][k+1])/Sigma[k])
            Ak2[j] = Pd[j][k]
            Ak3[j] = Point[k][j]
        sk = 0
        while (sk+ds) <= Sigma[k]:  # 描画
            sk += ds
            resultX.append(((Ak0[0]*sk+Ak1[0])*sk+Ak2[0])*sk+Ak3[0])
            resultY.append(((Ak0[1]*sk+Ak1[1])*sk+Ak2[1])*sk+Ak3[1])

    aAx.plot([p[0] for p in Point], [p[1] for p in Point], c="gray")
    aAx.plot(resultX, resultY, c="blue")


if __name__ == '__main__':
    """
    X = F(s) = a_x * s^3 + b_x * s^2 + c_x * s + d_x 
    Y = G(s) = a_y * s^3 + b_y * s^2 + c_Y * s + d_y 
    """
    Point = np.array([[0, 0], [0, 2], [2, 0], [2, 2]])
    #Point = np.array([[0, 0], [0, 2], [2, 2], [2, 0]])

    Sigma = [1, 1, 1]  # interval of parameter
    #Sigma = [1, 2, 1]

    P1d = [3, 3]  # X, Y differential at start
    Pnd = [3, 3]  # X, Y differential at end

    fig = plt.figure()
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)
    #ax3 = fig.add_subplot(3, 1, 3)

    Spline(Point, Sigma, P1d, Pnd, 0.01, True, ax1)
    Spline(Point, Sigma, P1d, Pnd, 0.01, False, ax2)

    fig.tight_layout()
    plt.show()
