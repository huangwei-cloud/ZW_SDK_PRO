import math

from ZW_RFAWG2000_PCIE import RFAWG2000_PCIE
from ctypes import c_int64
import numpy as np
import matplotlib.pyplot as plt
import math
import struct
import time

trigcnt = 32

param_dic = {
    "REG0Ctrl": 0x80000000,  # 控制寄存器
    "REG1PhaseParamDataLen": 0x5000,  # 相参数据长度
    "REG2AdCollectLen": 0xA00,  # AD采集数据长度
    "REG3AdCollectDelay": 0x60,  # ADC采集延时
    "REG4Dac1PlayLen": (trigcnt << 16) | 0x0C00,  # DAC1播放次数和播放个数
    "REG5Dac2PlayLen": (trigcnt << 16) | 0x0C00,  # DAC2播放次数和播放个数
    "REG6Dac3PlayLen": (trigcnt << 16) | 0x0C00,  # DAC3播放次数和播放个数
    "REG7Dac4PlayLen": (trigcnt << 16) | 0x0C00,  # DAC4播放次数和播放个数
    "REG8Dac5PlayLen": (trigcnt << 16) | 0x0C00,  # DAC5播放次数和播放个数
    "REG9Dac12PlayDelay": (0 << 16) | 0,  # DAC1,2播放延时
    "REG10Dac34PlayDelay": (0 << 16) | 0,  # DAC1,2播放延时
    "REG11Dac5PlayDelay": 0 << 16,  # 播放延时（DAC5）
    "REG12RefClkPhaseL32bit": 0x00000000,  # 参考信号相位低32位
    "REG13RefClkPhaseH16bit": 0x0001 << 16,  # 参考信号相位高16位
    "REG14RefClkFsL32bit": 0x00000000,  # 参考信号频率低32位
    "REG15RefClkFsH16bit": 0x1000,  # 参考信号频率高16位
}


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


def square_wave(A, f, phi, t):
    """
    :params A:    振幅[1,-1]
    :params f:    信号频率(Hz)[1,1e9]
    :params phi:   相位[0,360]
    :params t:    时间长度(秒)[1e-9,0.4]
    """
    fs = 8e+9
    Ts = 1 / fs
    n = t / Ts
    n = np.arange(n)
    x = A * np.sin(2 * np.pi * f * n * Ts + phi * (np.pi / 180))
    y = []
    for i in x:
        if np.sin(i) > 0:
            y.append(-1)
        else:
            y.append(1)
    return np.array(y)


dic_coeff = {
    "Coeffs0.Coeff0": 0xffd1ffe8,
    "Coeffs0.Coeff1": 0xffccfffe,
    "Coeffs0.Coeff2": 0x0037001f,
    "Coeffs0.Coeff3": 0xfffd000d,
    "Coeffs0.Coeff4": 0x00000000,
    "Coeffs0.Coeff5": 0x00000000,
    "Coeffs0.Coeff6": 0x00000000,
    "Coeffs0.Coeff7": 0x00000000,

    "Coeffs1.Coeff0": 0x003d003f,
    "Coeffs1.Coeff1": 0x005c0048,
    "Coeffs1.Coeff2": 0x00450061,
    "Coeffs1.Coeff3": 0x00440050,
    "Coeffs1.Coeff4": 0x00000000,
    "Coeffs1.Coeff5": 0x00000000,
    "Coeffs1.Coeff6": 0x00000000,
    "Coeffs1.Coeff7": 0x00000000,

    "Coeffs2.Coeff0": 0x00400000,
    "Coeffs2.Coeff1": 0x00500fae,
    "Coeffs2.Coeff2": 0x001f0fb8,
    "Coeffs2.Coeff3": 0x00240fda,
    "Coeffs2.Coeff4": 0x00000000,
    "Coeffs2.Coeff5": 0x00000000,
    "Coeffs2.Coeff6": 0x00000000,
    "Coeffs2.Coeff7": 0x00000000,

    "Coeffs3.Coeff0": 0x0021001c,
    "Coeffs3.Coeff1": 0x00210035,
    "Coeffs3.Coeff2": 0x000c0047,
    "Coeffs3.Coeff3": 0x00280045,
    "Coeffs3.Coeff4": 0x001d000f,
    "Coeffs3.Coeff5": 0x002c003e,
    "Coeffs3.Coeff6": 0x0004004c,
    "Coeffs3.Coeff7": 0x002b0046,
}

if __name__ == "__main__":
    # list1 = [1, 2]
    # list2 = [1, 5, 6, 4, 5]
    # z = list1 + list2
    # print(z)
    # x = []
    # for i in dic_coeff:
    #     x.append(dic_coeff[i])
    # y = np.asarray(x, np.uint32)
    # z = y.view("uint8")
    # print(z)
    obj = RFAWG2000_PCIE()

    obj.ethernet_connect("192.168.1.10", 7)

    obj.set_pcie_board_id(8)
    time.sleep(5)
    obj.set_coeff_verify(dic_coeff)
    # obj.setnbit(0x80040000, 0, 0xff)
    # obj.ethernet_connect("127.0.0.1", 7)
    #
    # obj.config_param(param_dic)
    #
    # # wave = generate_sin_waveform(A=1, f=4.25e+9, fs=8e+9, phi=90, t=20e-6) * (2 ** 15 - 1)
    # wave = square_wave(A=1, f=2e+8, phi=90, t=20e-6) * (2 ** 15 - 1)
    # x = 8e+9 * 20e-6
    # print(x)
    # x2 = range(int(x))
    # plt.title("send wave")
    # plt.plot(x2, wave)
    # plt.show()
    #
    # obj.send_dac_data(0, wave)
    # obj.send_dac_data(1, wave)
    # obj.send_dac_data(2, wave)
    # obj.send_dac_data(3, wave)
    #
    # # path = r"E:\Hw_work\ZYNQ\ZYNQ_RFAWG2000_PCIE\workspace\AWG2000_PCIE\src\xxx.bin"
    # # obj.send_dac_file(0, path)
    # # obj.send_dac_file(1, path)
    # # obj.send_dac_file(2, path)
    # # obj.send_dac_file(3, path)
    #
    # obj.dev_mem_write(0x80040000, 0, 0x80000020)  # open adc ch    bit 5
    # obj.dev_mem_write(0x80040000, 0, 0x80007C20)  # open dac ch	bit 10 - 14
    #
    # obj.dev_mem_write(0x80040000, 0, 0x800FFC20)  # open dac ch	bit 10 - 14
    #
    # obj.dac_play_user(trigcnt)
    # result = obj.get_iq_result_new(trigcnt)
    # buffer = np.reshape(result, (len(result)//2, 2))
    #
    # I = []
    # Q = []
    # z = []
    # for i in range(len(buffer)):
    #     I.append(buffer[i][0])
    #     Q.append(buffer[i][1])
    #     z.append(complex(buffer[i][0], buffer[i][1]))
    # mod = np.abs(z)
    # maxvalue = np.max(mod)
    # I2 = [i / maxvalue for i in I]
    # Q2 = [i / maxvalue for i in Q]
    #
    # plt.scatter(I2, Q2)
    # plt.show()

    # I = [-3450803978.0, -3448102463.0]
    # Q = [6146584732.0, 6140729167.0]
    # x = np.array(I, dtype=np.int64) ** 2
    # y = np.array(Q, dtype=np.int64) ** 2
    # print(x)
    # print(y)
    # z = []
    # for i in range(2):
    #     z.append(complex(I[i], Q[i]))
    # print(z)
    # # w = np.sqrt(x)
    # # z = np.sqrt((np.array(I, dtype=np.int) ** 2 + np.array(Q, dtype=np.int) ** 2))
    # w = np.abs(z)

    # H = 0xFFFFFFFF
    # L = 0xFF
    # I = H << 32 | L
    # print(I)
    # print(hex(I))
    # x = c_int64(I).value
    # print(x)
    # x = b'123456'
    # y = int(x)
    # print(y)

    # obj = RFAWG2000_PCIE()
    # obj.ethernet_connect("127.0.0.1", 8000)
    #
    # obj.send_dac_data(1, r"E:\Hw_work\Python\ZW_SDK_PRO\ZWDX_SDK\ZWDX_RF_AWG_PCIE\datafile0_4K.bin")

    # x = []
    # fd = open(r"E:\Hw_work\Python\ZW_SDK_PRO\ZWDX_SDK\ZWDX_RF_AWG_PCIE\datafile0_4K.bin", "rb")
    # x = fd.read(512)
    # y = np.frombuffer(x, dtype=np.uint8).tolist()
    # print(y)

    # x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # for i in range(len(x)//2):
    #     print(x[i*2:2*i+2])
    #
    # print(param_dic["PlayLen"])
    # templist = [(1, -2), (3, 4), (5, 6), (7, 8)]
    # x = []
    # y = []
    # for i in range(len(templist)):
    #     x.append(templist[i][0])
    #     y.append(templist[i][1])
    # plt.plot(x, y)
    # plt.show()

    # x = 512
    # y = np.asarray(512, np.uint32).byteswap()
    # z = int.from_bytes(y, "little")
    # print(hex(z))

    # fd = open(r"E:\Hw_work\ZYNQ\ZYNQ_RFAWG2000_PCIE\workspace\AWG2000_PCIE\src\test_data.h", 'r')
    # fdbin = open(r"E:\Hw_work\ZYNQ\ZYNQ_RFAWG2000_PCIE\workspace\AWG2000_PCIE\src\xxx.bin", 'wb')
    # fd.readline()
    # for i in range(163856):
    #     str = fd.readline()
    #     x = int(str[2:6], base=16)
    #     fdbin.write(struct.pack('H', x))
