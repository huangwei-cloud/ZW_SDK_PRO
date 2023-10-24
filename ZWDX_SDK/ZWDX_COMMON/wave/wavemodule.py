import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.fftpack import fft


def sin(A, fs, fsample, phi, t):
    """
    产生正弦波数据
    :param A:幅度
    :param t:采样时长(s)
    :param phi:相位,弧度制pi
    :param fs:频率(Hz)
    :param fsample:采样频率(Hz)
    :return:返回x,y轴元素数组, x是时间轴
    """
    x = np.linspace(0, t, int(fsample*t + 1))  # 时间0->t, 把时间等分，包含最后一个，这样写，最后会多采一个
    xx = x[0:-1] # 舍弃一个
    # x = np.arange(0, t, 1/fsample)  # 时间0->t, 每一个采样点的时间长度是1/采样频率， 不包含最后一个
    print(f'样点数量：{len(xx)}')
    yy = A*np.sin(2*np.pi*fs*xx + phi)
    return xx, yy


def generate_sin_waveform(A, f, fs, phi, t):
    """
    产生正弦波数据
    :param A: 归一化振幅，最大为1
    :param f: 信号频率 Hz
    :param fs: 采样频率 Hz
    :param phi: 相位，单位度
    :param t: 时间长度(秒)
    :return:
    """
    # 若时间序列长度为 t=1s,
    # 采样频率 fs=1000 Hz, 则采样时间间隔 Ts=1/fs=0.001s
    # 对于时间序列采样点个数为 n=t/Ts=1/0.001=1000, 即有1000个点,每个点间隔为 Ts
    Ts = 1 / fs
    n = t / Ts
    n = np.arange(n)
    temp = n*Ts
    temp2 = 2 * np.pi * f * (n * Ts)
    y = A * np.sin(2 * np.pi * f * (n * Ts) + phi * (np.pi / 180))

    return temp, y


if __name__ == '__main__':
    x, y = sin(1, 4.25e+9, 80e+9, 0, 10e-6)
    # plt.subplot(121)
    plt.plot(x, y)
    plt.show()

    xx, yy = generate_sin_waveform(1, 4.25e+9, 8e+9, 0, 10e-6)
    plt.plot(xx, yy)
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
