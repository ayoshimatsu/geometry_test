import numpy as np
import matplotlib.pyplot as plt


def setDT(N):  # データ設定
    DT = []
    for i in range(N+1):
        x = np.pi * i / 3
        DT.append([i, np.sin(x)])
    return DT

def cubicFormula(t,alfa):  #３次畳み込み関数による近似. interval 1.
    t1 = abs(t)
    t2 = t1 * t1
    t3 = t2 * t1
    if t1 >= 2:
        return 0
    if t1 >= 1:
        return alfa*t3 - 5*alfa*t2 + 8*alfa*t1 - 4*alfa
    return (alfa+2)*t3 - (alfa+3)*t2 + 1

def cubicInterpo(DT, alfa):  # 三次畳み込み関数による補間
    N = len(DT)
    R = []
    for i, point in enumerate(DT):
        for j in range(10):  # 0 ~ 0.9
            t = 0.1 * j
            V = DT[i][1] * cubicFormula(t, alfa)  # 0 ~1
            if i >= 1:
                V += DT[i-1][1] * cubicFormula(t+1, alfa)  # 1 ~ 2
            if i <= N-3:
                V += DT[i+2][1] * cubicFormula(t-2, alfa)  # 1 ~ 2
            if i <= N-2:
                V += DT[i+1][1] * cubicFormula(t-1, alfa)  # 0 ~ 1
            R.append([t+i, V])  # x, y coordinate
    return R


def standardDev(S):  # 標準偏差計算
    N=len(S)
    T=0
    for i in range(N):
        DY = np.sin(i*0.1*np.pi/3) - S[i][1]
        T += DY * DY
    return np.sqrt(T/N)


if __name__ == '__main__':
    start = -10 * np.pi
    DX = np.pi / 10

    DT = setDT(8)  # create original data
    plt.plot([p[0] for p in DT], [p[1] for p in DT], color="green")

    alfa = -0.6
    predictWave = cubicInterpo(DT, alfa)
    print(standardDev(predictWave))

    plt.plot([p[0] for p in predictWave], [p[1] for p in predictWave], color="red")
    plt.grid()
    plt.show()
