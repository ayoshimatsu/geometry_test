import numpy as np

def createSinWave(aTime, aT, aAmp, aPhase):
    """
    @param aTime: time [sec]
    @param aT: period [sec]
    @param aAmp: Amplitude
    @param aPhase: Phase [rad]
    @return: sin wave
    """
    return aAmp * np.sin(aTime * 2 * np.pi / aT + aPhase)

def createCosWave(aTime, aT, aAmp, aPhase):
    """
    @param aTime: time [sec]
    @param aT: period [sec]
    @param aAmp: Amplitude
    @param aPhase: Phase [rad]
    @return: sin wave
    """
    return aAmp * np.cos(aTime * 2 * np.pi / aT + aPhase)


def createSquareWaveFromSin(aTime, aWaveNumber):
    """
    Fourier series of square wave
    @param aTime: time data
    @param aWaveNumber: number of sin wave to sum up
    @return: y coordinate of wave
    """
    result = np.zeros_like(aTime)
    aTime = aTime * np.pi  # convert to (x * pi)
    for index, x in enumerate(aTime):
        for i in range(1, aWaveNumber, 1):
            result[index] += np.sin((2 * i - 1) * x) / (2 * i - 1)
        result[index] = result[index] * 4 / np.pi
    return result

def createTriangleWaveFromCos(aTime, aWaveNumber):
    result = np.zeros_like(aTime)
    aTime = aTime * np.pi  # convert to (x * pi)
    for index, t in enumerate(aTime):
        for i in range(1, aWaveNumber, 1):
            result[index] += np.cos((2 * i - 1) * t) / np.square(2 * i - 1)
    return result

def createSawToothWaveFromSin(aTime, aWaveNumber):
    result = np.zeros_like(aTime)
    aTime = aTime * np.pi  # convert to (x * pi)
    for index, t in enumerate(aTime):
        for i in range(1, aWaveNumber, 1):
            result[index] += np.power(-1, i+1) * np.sin(i * t) / i
        result[index] = result[index] * 2 / np.pi
    return result

def createQuadraticWave(aTime, aWaveNumber):
    result = np.zeros_like(aTime)
    aTime = aTime * np.pi  # convert to (x * pi)
    for index, t in enumerate(aTime):
        for i in range(1, aWaveNumber, 1):
            result[index] += np.power(-1, i+1) * np.cos(i * t) / (i**2)
        result[index] = np.pi**2 / 3 - 4 * result[index]
    return result

def createRepeatedLinearWave(aTime, aWaveNumber):
    result = np.zeros_like(aTime)
    aTime = aTime * np.pi  # convert to (x * pi)
    for index, t in enumerate(aTime):
        elementCos = 0
        elementSin = 0
        for i in range(1, aWaveNumber, 1):
            elementCos += np.cos((2 * i - 1) * t) / (np.square(2 * i - 1) * np.pi)
            elementSin += np.power(-1, i+1) * np.sin(i * t) / i
        result[index] = np.pi / 4 - (2 * elementCos - elementSin)
    return result

def createCubicWave(aTime, aWaveNumber):
    result = np.zeros_like(aTime)
    aTime = aTime * np.pi  # convert to (x * pi)
    for index, t in enumerate(aTime):
        for i in range(1, aWaveNumber, 1):
            result[index] += (2 * np.square(np.pi) / i - (12 / np.power(i, 3))) * np.power(-1, i+1) * np.sin(i * t)
    return result

def createStairWave(aTime, aWaveNumber):
    result = np.zeros_like(aTime)
    aTime = aTime * np.pi  # convert to (x * pi)
    for index, t in enumerate(aTime):
        elementCos = 0
        elementSin = 0
        for i in range(1, aWaveNumber, 1):
            elementCos += np.power(-1, i+1) * np.cos((2 * i - 1) * t) / (2 * i - 1)
            elementSin += (1 - np.power(-1, i)) * np.sin(2 * i * t) / i
        result[index] = - 2 / np.pi * elementCos - 1 / np.pi * elementSin
    return result
