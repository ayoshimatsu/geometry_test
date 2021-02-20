import math

def array(N1, N2 = 0):  # Create Array
    if N2 != 0:
        return [[0 for i in range(N2)] for i in range(N1)]
    return [0 for i in range(N1)]

# 以下，補間用プログラム
def setTerm(i, N, F):
    """
    (-1)^(N-i+1) * f(x_i) / (i-1)! / (N-i+1)!
    @param i: i th data
    @type i: int
    @param N: number of base data
    @type N: int
    @param F: base result of f(x) vector
    @type F: List of double
    @return: (-1)^(N-i+1) * f(x_i) / (i-1)! / (N-i+1)!
    @rtype: double
    """
    ii = 1
    for j in range(1, N-i+1):
        ii *= -1
    T = ii * F[i-1]  # T = ii * F[i-1] / (i-1)! / (N-i)!
    for k in range(1, i):  # calculate: (i-1)!
        T /= k
    for k in range(1, N-i+1):  # calculate: (N-i)!
        T /= k
    return T

def interp(i, N, UX):  # 補間計算
    """
    {u * (u-1) * ... * (u-(N-1))}. (u-i) is not multiplied.
    @param i: i th data
    @type i: int
    @param N: number of base data
    @type N: int
    @param UX: u
    @type UX: double
    @return: {u * (u-1) * ... * (u-(N-1))}. (u-i) is not multiplied.
    @rtype: double
    """
    U = UX
    result = 1
    for k in range(1, N+1):
        if i != k:
            result *= U
        U -= 1
    return result

def lagrangeInter(F, UX):
    """
    Calculate Lagrange interpolation.
    @param F: base result of f(x) vector
    @type F: List of double
    @param UX: width of target data / interval x
    @type UX: double
    @return: predicted result from interpolation
    @rtype: double
    """
    N = len(F)
    result =- F[0]
    for i in range(1, N+1):
        A = F[1-1]
        if i >= 2:
            A = setTerm(i, N, F) * interp(i, N, UX)  # f(x_i) * {u * (u-1) * ... * (u-(N-1))}
        result = result + A
    return result


if __name__ == '__main__':
    intervalOfYT = 10
    YT = [0, 0.17365, 0.34202, 0.5, 0.64279]
    X = lagrangeInter(YT, 22 / intervalOfYT)
    print("Result of interpolation:", X)
