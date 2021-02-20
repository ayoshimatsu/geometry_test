import numpy as np
import matplotlib.pyplot as plt

def base_wave(X):
    return np.sin(X/2) - np.sin(X)

def sampling(aX_list, aY_list, aInterval, aAx):  # データ表示
    tempX = aX_list[0]
    tempY = aY_list[0]
    sample_list = []
    for index, x in enumerate(aX_list):
        if (index % aInterval) == 0:
            aAx.plot([tempX, aX_list[index]], [tempY, tempY], color="blue")
            aAx.vlines(x=aX_list[index], ymin=tempY, ymax=aY_list[index], colors="blue")
            #aAx.vlines(x=x, ymin=tempY, ymax=aY_list[index], colors="blue")
            tempX = aX_list[index]
            tempY = aY_list[index]
        sample_list.append([x, tempY])
    return sample_list

def average(aSampleHold, i, aAverageNum):
    ist = i - aAverageNum + 1
    T = 0
    if ist < 0:
        ist = 0
    for k in range(ist, i+1):
        T += aSampleHold[k][1]  # average of y_coordinate
    return T / aAverageNum

def averageSampleHold(aSampleHold, aAverageNum):  # 多段階平均化による低域フィルタ
    """
    One of low pass filter
    @param aSampleHold:
    @param aAverageNum:
    @return:
    """
    average_result = []
    for i in range(aAverageNum):
        average_result.append([aSampleHold[0]])

    for sample_index, sample in enumerate(aSampleHold):
        if sample_index == 0:
            continue
        for ave_index, ave in enumerate(average_result):
            if ave_index == 0:
                ave.append([sample[0], average(aSampleHold, sample_index, aAverageNum)])
            else:
                ave.append([sample[0], average(average_result[ave_index-1], sample_index, aAverageNum)])
    return average_result


"""
def dspSH2(canvas, S):#多段階平均化によるLPF(その2)
    X1=0; DX=math.pi/20;M=20; A=array(M,2)
    for i in range(1, 120):
        A[0][1]=(S[i-1]+S[i])/2
        for j in range(1,M): 
            A[j][1]=(A[j-1][0]+A[j-1][1])/2
        X2=X1+DX; 
        drawDT(canvas, X1,S[i-1],X2,S[i],2,'#770077')
        for j in range(0,M-1,3):
            drawDT(canvas, X1,A[j][0],X2,A[j][1],1,'green')
        drawDT(canvas, X1,A[M-1][0],X2,A[M-1][1],3,'Blue')
        X1=X2
        for j in range(M):A[j][0]=A[j][1]
"""

def binaryAverageSampleHold(aSampleHold, aBinaryNum):
    A = np.zeros([aBinaryNum, 2])
    result = []
    # result.append(aSampleHold[0])
    for index, sample in enumerate(aSampleHold):
        A[0][1] = (aSampleHold[index-1][1] + sampleHoldList[index][1]) / 2
        for j in range(1, aBinaryNum):  # repetition of binarization
            A[j][1] = (A[j-1][0] + A[j-1][1]) / 2
        result.append([sample[0], A[aBinaryNum-1][1]])  # x, y coordinate
        for j in range(aBinaryNum):
            A[j][0] = A[j][1]
    return result


if __name__ == '__main__':
    start = 0
    DX = np.pi / 20
    x_data = np.arange(start, 20+DX, DX)  # x for display
    y_data = base_wave(x_data)

    fig = plt.figure()
    ax1 = fig.add_subplot(2, 1, 1)
    ax2 = fig.add_subplot(2, 1, 2)
    ax1.plot(x_data, y_data, color="red")  # original wave
    ax2.plot(x_data, y_data, color="red")  # original wave

    samplingNumber = 5
    sampleHoldList = sampling(x_data, y_data, samplingNumber, ax1)  # sampling
    sampleHoldList = sampling(x_data, y_data, samplingNumber, ax2)  # sampling

    # print(sampleHoldList)

    averageNumber = 4
    averageWaveList = averageSampleHold(sampleHoldList, averageNumber)  # easy low pass filter

    binaryNumber = 20
    binaryWaveList = binaryAverageSampleHold(sampleHoldList, binaryNumber)  # binary calculation

    for index, averageList in enumerate(averageWaveList):
        if index == averageNumber - 1:
            ax1.plot([p[0] for p in averageList], [p[1] for p in averageList])  # average wave result
        else:
            ax1.plot([p[0] for p in averageList], [p[1] for p in averageList], linestyle="--")
    ax1.grid(True)

    ax2.plot([p[0] for p in binaryWaveList], [p[1] for p in binaryWaveList], color="green")
    ax2.grid(True)

    plt.show()
