import ZW_RF_AWG1000
import numpy as np
from matplotlib import pyplot as plt


def generate_sin_waveform(A, f, fs, phi, t):
    """
    产生正弦波数据
    :param A: 振幅
    :param f: 信号频率Hz
    :param fs: 采样频率Hz
    :param phi: 相位
    :param t: 时间长度秒(s)
    :return: 
    """
    # 若时间序列长度为 t=1s,
    # 采样频率 fs=1000 Hz, 则采样时间间隔 Ts=1/fs=0.001s
    # 对于时间序列采样点个数为 n=t/Ts=1/0.001=1000, 即有1000个点,每个点间隔为 Ts
    Ts = 1 / fs
    n = t / Ts
    n = np.arange(n)
    y = A * np.sin(2 * np.pi * f * n * Ts + phi * (np.pi / 180))
    return y


def generate_square_waveform(A, f, fs, phi, t):
    """
    产生方波数据
    :param A:振幅
    :param f:信号频率Hz
    :param fs:采样频率Hz
    :param phi:相位
    :param t:时间长度秒（s）
    :return:
    """
    x = generate_sin_waveform(A, f, fs, phi, t)
    y = []
    for i in x:
        if np.sin(i) > 0:
            y.append(-1)
        else:
            y.append(1)
    return np.array(y)


if __name__ == "__main__":
    handle = ZW_RF_AWG1000.RF_AWG1000()

    handle.connect("192.168.1.2", 9003)  # 连接设备

    handle.set_refclk("ext_ref", 100)  # 设置外参考100M

    handle.set_sampling_rate("5G")  # 设置采样率为5G采样

    handle.set_mode_switch("NRZ")  # 模式切换

    handle.set_play_mode("continue")  # 设置播放模式为连续播放模式

    handle.set_channel_delay(1, 200 * 1e-12)  # 设置通道一延时200ps

    handle.open_channel([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])  # 打开通道

    handle.close_channel([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])  # 关闭通道

    handle.send_waveform_file(r"F:\FPGA\xf\07_9162\doc\data\Waveform_ad9162_ch1_sin100m.dat")  # 发送波形文件

    handle.send_waveform_data(generate_sin_waveform(A=1, f=50e+6, fs=5e+9, phi=0, t=200e-9))  # 发送波形数据

    handle.set_ip("192.168.0.100")  # 更改设备IP

    handle.disconnect()  # 断开设备连接

    # 以下为画波形测试,客户不用关心这部分,可以使用jupyter观看画出的波形

    # 画正弦波
    # f=50 hz
    fsample = 5000
    hz_50 = generate_sin_waveform(A=1, f=50, fs=fsample, phi=0, t=0.08)
    hz_50_30 = generate_sin_waveform(A=1, f=50, fs=fsample, phi=30, t=0.08)
    hz_50_60 = generate_sin_waveform(A=1, f=50, fs=fsample, phi=60, t=0.08)
    hz_50_90 = generate_sin_waveform(A=1, f=50, fs=fsample, phi=90, t=0.08)
    x = np.arange(0, 0.08, 1 / fsample)
    plt.xlabel('t/s')
    plt.ylabel('y')
    plt.grid()
    plt.plot(x, hz_50, 'k')
    plt.plot(x, hz_50_30, 'r-.')
    plt.plot(x, hz_50_60, 'g--')
    plt.plot(x, hz_50_90, 'b-.')
    plt.legend(['phase 0', 'phase 30', 'phase 60', 'phase 90'], loc=1)
    plt.show()

    # 画方波(RF_AWG1000不能输出方波)
    yy = generate_square_waveform(A=1, f=50, fs=fsample, phi=0, t=0.08)
    x = np.arange(0, 0.08, 1 / fsample)
    plt.plot(x, yy)
    plt.show()
