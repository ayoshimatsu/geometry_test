import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    t = np.arange(0, np.pi * 10, 0.01)
    x = t * np.cos(t)
    y = t * np.sin(t)

    plt.plot(x, y, color="blue")
    plt.grid(True)
    plt.show()
