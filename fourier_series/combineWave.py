import numpy as np
import matplotlib.pyplot as plt
import fourier_series.waveSynthesisHelper as helper


if __name__ == '__main__':
    t_data = np.arange(-2, 2 + 0.02, 0.02)

    """
    sinWaveA = helper.createSinWave(t_data, 2, 1, 0)
    sinWaveB = helper.createSinWave(t_data, 1, 1, 0)
    sinWaveAB = sinWaveA + sinWaveB
    square = helper.createSquareWaveFromSin(t_data, 200)
    triangle = helper.createTriangleWaveFromCos(t_data, 100)
    sawTooth = helper.createSawToothWaveFromSin(t_data, 100)
    quadratic = helper.createQuadraticWave(t_data, 100)
    linear = helper.createRepeatedLinearWave(t_data, 500)
    cubic = helper.createCubicWave(t_data, 100)
    """

    stair = helper.createStairWave(t_data, 500)

    fig = plt.figure()
    #ax1 = fig.add_subplot(1, 2, 1)
    #ax2 = fig.add_subplot(1, 2, 2)
    plt.plot(t_data, stair, color="red")
    # plt.plot(t_data, sinWaveA, color="green", linestyle="--")
    # plt.plot(t_data, sinWaveB, color="blue", linestyle="--")
    # plt.plot(t_data, sinWaveAB, color="red")

    plt.grid()
    plt.show()
