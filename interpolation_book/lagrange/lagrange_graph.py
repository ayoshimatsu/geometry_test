from interpolation_book.lagrange import lagrange_interpolation as lag
import numpy as np
import matplotlib.pyplot as plt

def logisticFormula(k, m, a, t):
    """
    logistic curve.
    y(t) = k / (1 + m * exp(-a*t))
    """
    return k / (1 + m * np.exp(-a*t))

def setDisContinuousLine(aX):
    y = lag.array(len(aX))
    for index, element in enumerate(aX):
        if index <= 50:
            y[index] = element * 0.2 + 5
        else:
            y[index] = (element - 5) * 0.2 + 5
    return y

def loopLagrangeInter(aPredictX, aInterpolateY, aXInterval):
    result = []
    for index, element in enumerate(aPredictX):
        u = element / aXInterval
        result.append(lag.lagrangeInter(aInterpolateY, u))
    return result


if __name__ == '__main__':
    x_data = np.arange(0, 10.1, 0.1)  # x data list
    x_intervalOfDataIndex = 10
    x_intervalOfValue = x_intervalOfDataIndex * 0.1
    base_x = x_data[0:len(x_data):x_intervalOfDataIndex]
    print(base_x)
    # draw logistic curve
    logistic_y = logisticFormula(k=1, m=100, a=1.5, t=x_data)  # logistic data list
    # draw predicted result calculated by interpolation
    interpolate_log = logistic_y[0:len(logistic_y):x_intervalOfDataIndex]
    predict_x = np.arange(0, 10.1, 0.1)  # x for predication
    predict_log = loopLagrangeInter(predict_x, interpolate_log, x_intervalOfValue)
    # draw discontinuous line
    discontinue_y = setDisContinuousLine(x_data)  # discontinuous data list
    interpolate_dis = discontinue_y[0:len(discontinue_y):x_intervalOfDataIndex]
    predict_x = np.arange(0, 10.1, 0.1)  # x for predication
    predict_dis = loopLagrangeInter(predict_x, interpolate_dis, x_intervalOfValue)
    # draw graph
    plt.plot(x_data, logistic_y)
    plt.plot(predict_x, predict_log)
    #plt.plot(x_data, discontinue_y)
    #plt.plot(predict_x, predict_dis)
    plt.ylim(-0.5, 1.5)
    plt.grid(True)
    plt.show()
