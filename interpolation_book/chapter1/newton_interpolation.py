def array_func(aNum1: int, aNum2=0):
    if aNum2 != 0:
        return [[0 for _ in range(aNum2)] for _ in range(aNum1)]
    return [0 for _ in range(aNum1)]

def comb(N, R):  # calculate combination. nCr
    if R == 0 or R == N:
        return 1
    if R == 1:
        return N
    return comb(N-1, R-1) + comb(N-1, R)

def comb2(N, R):  # improved method of comb
    A = array_func(N)
    NN = N
    RR = R
    if (NN - RR) < RR:
        RR = N - R
    if RR == 0: return 1
    if RR == 1: return N
    for i in range(2, RR + 1):
        A[i-1] = i + 1
        print(A)
    for i in range(1, NN - R):
        A[0] = i + 2
        print(i)
        for j in range(2, RR + 1):
            A[j - 1] = A[j - 2] + A[j - 1]
            print(A)
    return A[RR - 1]

def setParam(F):
    """
    On the premise that data is set at regular intervals.
    @param F: result y
    @type F: list
    @return: coefficient list
    @rtype: list
    """
    N = len(F)
    A = array_func(N)
    for i in range(N):
        C = F[i]
        SG = -1
        for j in range(i-1, 0, -1):
            CB = comb2(i, j)
            C += SG*CB*F[j]
            SG = -SG
        for k in range(1, i+1):
            C /= k  # i! で除す処理
        A[i] = C
    return A

def gregoryTest(F, UX):
    """
    Gregory newton interpolation.
    On the premise that data is set at regular intervals.
    x = x1 + u*h
    @param F: result Y
    @type F: list
    @param UX: interval of U. x = x1 + U*h. x1 = 0. h = 10.
    @type UX: double
    @return: prediction value
    @rtype: double
    """
    A = setParam(F)  # coefficient list
    N = len(A)
    T = 0  # 各項目の計算とトータルの計算
    for i in range(N):
        D = UX
        FX = A[i]
        for j in range(i):
            FX *= D
            D -= 1
        T += FX
    return T


if __name__ == '__main__':
    comb2(10, 4)
    XT = [0, 10, 20, 30, 40]
    YT = [0, 0.17365, 0.34202, 0.5, 0.64279]
    result = gregoryTest(YT, 22/10)  # x1 = 0. h = 10. x = 22. In the case of XT.
    print("Result", result)
