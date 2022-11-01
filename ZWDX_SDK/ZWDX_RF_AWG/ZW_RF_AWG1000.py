import socket
import numpy as np
import struct

g_ch_status = 0


class ref_clk_cmd:
    head = 0x18EFDC01
    cmd_type = 0x01
    input_clk = 00
    yuliu = np.zeros(6, dtype=np.uint8)
    end = 0x01DCEF18

    def __init__(self, ref: str, freq):
        if ref == 'ext_ref':
            if freq == 10:
                self.input_clk = 0
            elif freq == 100:
                self.input_clk = 1
            else:
                pass
        elif ref == 'int_ref':
            if freq == 100:
                self.input_clk = 2
            else:
                pass
        else:
            print(f'input param error...')

    def build(self):
        format_str = '!IBB6sI'
        string = struct.pack(format_str, self.head, self.cmd_type, self.input_clk, self.yuliu.tobytes(), self.end)
        return string


class tcp_down_cmd:
    head = 0x18EFDC01
    cmd_type = 2
    ch = 1
    yuliu = np.zeros((6,), np.int8)
    wave_data = []
    end = 0x01DCEF18

    def __init__(self, ch, data):
        self.ch = ch
        if type(data[0]) == np.int8:
            self.length = len(data)
        elif type(data[0]) == np.int16:
            self.length = len(data) * 2
        else:
            print('error')
        self.wave_data = data

    def build(self):
        format_str = '!IBB6s' + str(self.length) + 's' + 'I'
        ss = struct.pack(format_str, self.head, self.cmd_type, self.ch,
                         self.yuliu.tobytes(), np.asarray(self.wave_data).tobytes(), self.end)

        return ss


class sampling_rate_cmd:
    head = 0x18EFDC01
    cmd_type = 0x03
    cai_yang_lv = 0
    yuliu = np.zeros(6, dtype=np.uint8)
    end = 0x01DCEF18

    def build(self):
        return struct.pack('!IBB6sI', self.head, self.cmd_type, self.cai_yang_lv, self.yuliu.tobytes(), self.end)


class mo_shi_switch:
    head = 0x18EFDC01
    cmd_type = 0x04
    mode = 0
    yuliu = np.zeros(6, dtype=np.uint8)
    end = 0x01DCEF18

    def build(self):
        return struct.pack('!IBB6sI', self.head, self.cmd_type, self.mode, self.yuliu.tobytes(), self.end)


class tcp_open_cmd:
    head = 0x18EFDC01
    cmd_type = 5
    ch = 0x0FFF
    yuliu = np.zeros((5,), np.int8)
    end = 0x01DCEF18

    def __init__(self, ch_list, operation='open'):
        global g_ch_status
        if operation == 'open':
            for i in ch_list:
                g_ch_status |= (1 << (i - 1))
        else:
            for i in ch_list:
                g_ch_status &= ~(1 << (i - 1))
        self.ch = g_ch_status

    def build(self):
        format_str = '!IBH5sI'
        ss = struct.pack(format_str, self.head, self.cmd_type, self.ch, self.yuliu.tobytes(), self.end)
        return ss


class tcp_mai_chong_switch_cmd:
    head = 0x18EFDC01
    cmd_type = 6
    mode = 0
    yuliu = np.zeros((6,), np.int8)
    end = 0x01DCEF18

    def __init__(self, mode=0):
        self.mode = mode

    def build(self):
        format_str = '!IBB6sI'
        ss = struct.pack(format_str, self.head, self.cmd_type, self.mode, self.yuliu.tobytes(), self.end)
        return ss


class tcp_ip_switch_cmd:
    head = 0x18EFDC01
    cmd_type = 7
    ip = []
    yuliu = np.zeros((3,), np.int8)
    end = 0x01DCEF18

    def __init__(self, ip=''):
        self.ip.clear()
        list = ip.split('.')
        for i in list:
            self.ip.append(int(i))

    def build(self):
        format_str = '!IB4s3sI'
        ss = struct.pack(format_str, self.head, self.cmd_type, np.asarray(self.ip, np.uint8).tobytes(),
                         self.yuliu.tobytes(), self.end)
        return ss


class sleep_control:
    head = 0x18EFDC01
    cmd_type = 0x08
    ch = 1
    delay = 0x00000000
    yuliu = np.zeros(2, dtype=np.uint8)
    end = 0x01DCEF18

    def build(self):
        return struct.pack('!IBBI2sI', self.head, self.cmd_type, self.ch, self.delay, self.yuliu.tobytes(), self.end)


class RF_AWG1000:

    def __init__(self):
        self.s = None

    def __del__(self):
        if self.s is not None:
            self.s.close()

    def connect(self, ip: str, port: int):
        """
        以太网连接设备
        :param ip: IP地址
        :param port: 端口号
        :return:
        """
        self.s = socket.socket()
        self.s.connect((ip, port))

    def disconnect(self):
        """
        以太网断开连接
        :return:
        """
        if self.s is not None:
            self.s.close()

    def get_ack_status(self):
        msg = self.s.recv(16)
        format_str = '!IBB6sI'
        head, type, ack, yuliu, end = struct.unpack(format_str, msg)
        if ack == 0xAA:
            return True
        else:
            return False

    def set_refclk(self, ref_config: str, freq_config: str):
        """
        时钟控制之设置参考钟
        :param ref_config:”int_ref“:内参考 ”ext_ref“:外参考
        :param freq_config:频率值（MHz）常用10MHz, 100MHz
        :return:
        """
        cmd = ref_clk_cmd(ref_config, freq_config)
        self.s.send(cmd.build())
        return self.get_ack_status()

    def set_sampling_rate(self, sp: str):
        """
        设置采样率
        :param sp: “5G”:5g采样率 “4G”:4g采样率
        :return:
        """
        cmd = sampling_rate_cmd()
        if sp == '5G':
            cmd.cai_yang_lv = 0
        elif sp == '4G':
            cmd.cai_yang_lv = 1
        else:
            print(f"input param error...")
        self.s.send(cmd.build())
        return self.get_ack_status()

    def set_mode_switch(self, mode: str):
        """
        模式切换
        :param mode:“NRZ” :NRZ模式 “MIX”:MIX模式
        :return:
        """
        cmd = mo_shi_switch()
        if mode == 'NRZ':
            cmd.mode = 0
        elif mode == 'MIX':
            cmd.mode = 1
        else:
            pass
        self.s.send(cmd.build())
        return self.get_ack_status()

    def set_channel_delay(self, ch, time: int):
        """
        设置通道延时
        :param ch:通道号
        :param time:延时值，单位秒(s), 步进延时为200ps
        :return:
        """
        cmd = sleep_control()
        cmd.ch = ch
        x = (time * 1e+12) % 200
        if x != 0:
            print(f"input param not 200ps integral multiple...")
            return

        cmd.delay = (time * 1e+12) // 200
        self.s.send(cmd.build())
        return self.get_ack_status()

    def open_channel(self, ch_list):
        """
        打开通道【1-12】
        :param ch_list:需要打开的通道列表 example:[1,5,7]
        :return: 返回打开是否成功状态
        """
        cmd = tcp_open_cmd(ch_list)
        self.s.send(cmd.build())
        return self.get_ack_status()

    def close_channel(self, ch_list):
        """
        关闭通道【1-12】
        :param ch_list:需要关闭的通道列表 example:[2,5,7,10]
        :return:返回关闭是否成功状态
        """
        cmd = tcp_open_cmd(ch_list, 'close')
        self.s.send(cmd.build())
        return self.get_ack_status()

    def send_waveform_file(self, path):
        """
        发送波形文件
        :param path: 文件路径
        :return:
        """
        fd = open(path, 'rb')
        self.s.send(np.fromfile(fd, np.uint8))
        return self.get_ack_status()

    def send_waveform_data(self, ch, data):
        """
        发送波形数据
        :param ch: 通道
        :param data: 数据
        :return:
        """
        yushu = len(data) % 16
        if yushu:
            cha = 16 - yushu
            a = np.zeros(cha, dtype=np.int8)
            data = np.append(data, a)
        array = np.asarray(data).clip(-1, 1)
        point = array * (2 ** 15 - 1)
        u16point = np.asarray(point, dtype=np.int16).byteswap()
        self.s.send(tcp_down_cmd(ch, u16point).build())
        return self.get_ack_status()

    def set_ip(self, ip: str):
        """
        设置板卡IP重启后生效
        :param ip: IP地址
        :return:返回设置是否成功状态
        """
        cmd = tcp_ip_switch_cmd(ip)
        self.s.send(cmd.build())
        return self.get_ack_status()

    def set_play_mode(self, mode: str):
        """
        设置播放模式
        :param mode:”continue“:连续播放模式 ”pulse“:脉冲播放模式
        :return:
        """
        cmd = tcp_mai_chong_switch_cmd(mode)
        self.s.send(cmd.build())
        return self.get_ack_status()
