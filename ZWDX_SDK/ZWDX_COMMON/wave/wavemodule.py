import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.fftpack import fft


def sin(A, t, phi, fs, fsample):
    """
    产生正弦波数据
    :param A:幅度
    :param t:采样时长(s)
    :param phi:相位,弧度制
    :param fs:频率(Hz)
    :param fsample:采样频率(Hz)
    :return:返回x,y轴元素数组
    """
    x = np.linspace(0, t, int(fsample*t))
    y = A*np.sin(2*np.pi*fs*x + phi)
    return x, y


if __name__ == '__main__':
    x, y = sin(1, 2/500, 0, 500, 8000)
    plt.subplot(121)
    plt.plot(x, y)

    # plt.subplot(122)
    # window = signal.windows.hann(int(2 * 2000))
    # fft_y = fft(y*window)
    # abs_y = abs(fft_y)
    # x = np.arange(0, 2*2000) / 2
    # plt.plot(x, abs_y)
    #
    # max_index = np.argmax(abs_y)
    # fs = max_index * 2000 / (2 * 2000)
    # print(fs)
    plt.show()
