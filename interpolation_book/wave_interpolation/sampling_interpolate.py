import numpy as np
import matplotlib.pyplot as plt

def sinc(X):
    if abs(X) < 1E-30:
        return 1
    return np.sin(X) / X

def synthesis(aDt, aX):  #
    result = 0
    for i in range(len(aDt)):
        result += aDt[i] * sinc(aX - np.pi * i)
    return result


if __name__ == '__main__':
    st = -10 * np.pi
    DX = np.pi / 10

    x_data = np.arange(st, 30+DX, DX)  # x for display
    y_sinc_data = []  # basic sampling wave.
    for x in x_data:
        y_sinc_data.append(sinc(x))

    # y coordinate of predict point
    # In this case, these point is located at pi interval.
    y_predict = [0.2, 0.625, 0.625, -0.2, -0.625, -0.625, 0.2, 0.625]  # y coordinate of predict point

    for y_index, y_pre in enumerate(y_predict):
        y_sample_wave = []
        gap = y_index * np.pi
        plt.scatter(gap, y_pre, c="red")
        for x in x_data:
            y_sample_wave.append(y_pre * sinc(x-gap))
        plt.plot(x_data, y_sample_wave)

    y_synthesis = []
    for x in x_data:
        y_synthesis.append(synthesis(y_predict, x))

    # plt.plot(x_data, y_sinc_data)
    plt.plot(x_data, y_synthesis, linestyle="--")
    #plt.plot(x_data, np.sin(x_data), linestyle="--")

    plt.xlim(-5, 30)

    print(np.sin(np.pi))
    print(np.sin(np.pi / 2))

    plt.show()

