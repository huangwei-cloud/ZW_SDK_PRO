import socket
import numpy as np
import struct
import serial

g_ch_status = 0


class tcp_down_cmd:
    head = 0x18EFDC01
    cmd_type = 0x10
    ch = 1
    wave_point_cnt = 0x00000000
    da_default = 0x0000
    yuliu = np.zeros((4,), np.int8)
    wave_data = []
    yuliu1 = np.zeros((8,), np.int8)
    end1 = 0x01DCEF18
    end2 = 0x01DCEF18

    def __init__(self, ch, data):
        self.ch = ch
        if type(data[0]) == np.uint8:
            self.length = len(data)
        elif type(data[0]) == np.uint16:
            self.length = len(data) * 2
        else:
            print('error')
        self.wave_data = data

    def build(self):
        format_str = '!IBBIH4s' + str(self.length) + 's' + '8sII'
        ss = struct.pack(format_str, self.head, self.cmd_type, self.ch, self.wave_point_cnt, self.da_default,
                         self.yuliu.tobytes(), np.asarray(self.wave_data).tobytes(), self.yuliu1.tobytes(), self.end1,
                         self.end2)

        return ss


class tcp_open_cmd:
    head = 0x18EFDC01
    cmd_type = 2
    ch = 0x00
    yuliu = np.zeros((6,), np.int8)
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
        print(f'open ch = {self.ch}')

    def build(self):
        format_str = '!IBB6sI'
        ss = struct.pack(format_str, self.head, self.cmd_type, self.ch, self.yuliu.tobytes(), self.end)
        return ss


class tcp_data_source_cmd:
    head = 0x18EFDC01
    cmd_type = 3
    mode = 0
    ftw = 0
    yuliu = np.zeros((4,), np.int8)
    end = 0x01DCEF18

    def __init__(self, ftw, mode=0):
        self.mode = mode
        self.ftw = ftw

    def build(self):
        format_str = '!IBBH4sI'
        ss = struct.pack(format_str, self.head, self.cmd_type, self.mode, self.ftw, self.yuliu.tobytes(), self.end)
        return ss


class tcp_ref_switch_cmd:
    head = 0x18EFDC01
    cmd_type = 4
    ref = 0x00
    clk = None
    yuliu = np.zeros((5,), np.int8)
    end = 0x01DCEF18

    def __init__(self, ref: str, freq):
        if ref == 'ext_ref':
            self.ref = 0x01
        elif ref == 'int_ref':
            self.ref = 0x00
        else:
            print(f'input error')
        self.clk = freq

    def build(self):
        format_str = '!IBB5sI'
        ss = struct.pack(format_str, self.head, self.cmd_type, self.ref, self.clk,
                         self.yuliu.tobytes(), self.end)
        return ss


class tcp_attenuation_cmd:
    head = 0x18EFDC01
    cmd_type = 5
    ch = 0x01
    atten = 0x00
    yuliu = np.zeros((5,), np.int8)
    end = 0x01DCEF18

    def __init__(self, ch, db):
        self.ch = ch
        self.atten = db

    def build(self):
        return struct.pack('!IBBB5sI', self.head, self.cmd_type, self.ch, self.atten, self.yuliu.tobytes(), self.end)


class tcp_output_mode_cmd:
    head = 0x18EFDC01
    cmd_type = 6
    ch = 0x01
    mode = 0x00
    yuliu = np.zeros((5,), np.int8)
    end = 0x01DCEF18

    def __init__(self, ch: int, mode: str):
        self.ch = ch
        if mode == "AC":
            self.mode = 0x00
        elif mode == "DC":
            self.mode = 0x01
        else:
            pass

    def build(self):
        return struct.pack('!IBBB5sI', self.head, self.cmd_type, self.ch, self.mode, self.yuliu.tobytes(), self.end)


class tcp_ch_tiggerselect_cmd:
    head = 0x18EFDC01
    cmd_type = 7
    ch = 0x00
    ch_trigger = 0x00
    trigger_delay_cu = 0x00000000
    trigger_delay_xi = 0x00
    markout_delay = 0x00000000
    yuliu = np.zeros((12,), np.int8)
    end = 0x01DCEF18

    def __init__(self):
        pass

    def build(self):
        return struct.pack('!IBBBIBI12sI', self.head, self.cmd_type, self.ch,
                           self.ch_trigger, self.trigger_delay_cu, self.trigger_delay_xi,
                           self.markout_delay, self.yuliu.tobytes(), self.end)


class tcp_fan_ctrl_cmd:
    head = 0x18EFDC01
    cmd_type = 8
    speed = 0x0000
    yuliu = np.zeros((5,), np.int8)
    end = 0x01DCEF18

    def __init__(self):
        pass

    def build(self):
        return struct.pack('!IBH5sI', self.head, self.cmd_type, self.speed, self.yuliu.tobytes(), self.end)


class tcp_get_temp_cmd:
    head = 0x18EFDC01
    cmd_type = 9
    yuliu = np.zeros((7,), np.int8)
    end = 0x01DCEF18

    def __init__(self):
        pass

    def build(self):
        return struct.pack('!IB7sI', self.head, self.cmd_type, self.yuliu.tobytes(), self.end)


class tcp_set_ip_cmd:
    head = 0x18EFDC01
    cmd_type = 0x11
    ip = []
    yuliu = np.zeros(3, np.uint8)
    end = 0x01DCEF18

    def __init__(self, ip=''):
        ip_list = ip.split('.')
        for i in ip_list:
            self.ip.append(int(i))

    def build(self):
        return struct.pack('!IB4s3sI', self.head, self.cmd_type, np.asarray(self.ip, np.uint8).tobytes(),
                           self.yuliu.tobytes(), self.end)


class tcp_da_default_cmd:
    head = 0x18EFDC01
    cmd_type = 0x12
    channel = 0
    default = 0
    yuliu = np.zeros(5, np.uint8)
    end = 0x01DCEF18

    def __init__(self):
        pass

    def build(self):
        return struct.pack('!IBBB5sI', self.head, self.cmd_type, self.channel, self.default,
                           self.yuliu.tobytes(), self.end)


class AWG1000:
    def __init__(self):
        self.s = None
        self.u = None

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

    def open_uart(self, com: str):
        """
        打开串口
        :param com: 串口号
        :return:
        """
        try:
            self.u = serial.Serial(com, 115200, stopbits=1, bytesize=8, parity='N', timeout=5)
        except serial.SerialException:
            print("Is com port being used by other application?")

    def close_uart(self):
        """
        关闭串口
        :return:
        """
        if self.u is not None:
            self.u.close()

    def get_ack_status(self, x=0):
        if x == 0:
            msg = self.s.recv(16)
        else:
            msg = self.u.read(16)
        format_str = '!IBB6sI'
        head, type, ack, yuliu, end = struct.unpack(format_str, msg)
        if ack == 0xAA:
            return True
        else:
            return False

    def change_dev_ip(self, mode: str, ip: str):
        """
        以太网或着串口方式更改设备IP
        :param mode: "eth":以太网 ”uart“:串口
        :param ip: ip地址，eg:"192.168.1.10"
        :return:
        """
        cmd = tcp_set_ip_cmd(ip)
        if mode == "eth":
            if self.s is not None:
                self.s.send(cmd.build())
                return self.get_ack_status()
            else:
                print(f"ethernet disconnect...")
        else:
            if self.u is not None:
                self.u.write(cmd.build())
                return self.get_ack_status(1)
            else:
                print(f"uart not open...")
        return False

    def get_dev_ip(self):
        """
        通过串口获取设备IP
        :return: 返回设备IP
        """
        ip = None
        frame = [0x55, 0x01, 0, 0, 0, 0, 0, 0xAA]
        if self.u is None:
            print(f"uart not open...")
            return
        self.u.write(frame)
        msg = self.u.read(8)
        if len(msg) == 8:
            ip = f'{msg[2]}.{msg[3]}.{msg[4]}.{msg[5]}'
        return ip

    def open_channel(self, ch: list):
        """
        打开通道
        :param ch:需要打开的通道列表， eg:[1,5]
        :return:返回执行状态（bool）
        """
        cmd = tcp_open_cmd(ch)
        self.s.send(cmd.build())
        return self.get_ack_status()

    def close_channel(self, ch: list):
        """
        关闭通道
        :param ch:需要关闭的通道列表， eg:[1,5]
        :return:返回执行状态
        """
        cmd = tcp_open_cmd(ch, 'close')
        self.s.send(cmd.build())
        return self.get_ack_status()

    def set_refclk(self, ref_config: str, freq_config: str):
        """
        参考钟设置
        :param ref_config: ”int_ref“:内参考 ”ext_ref“:外参考
        :param freq_config: 频率值（MHz）常用10MHz, 100MHz
        :return:
        """
        cmd = tcp_ref_switch_cmd(ref_config, freq_config)
        self.s.send(cmd.build())
        return self.get_ack_status()

    def send_wave(self, data, ch):
        cmd = tcp_down_cmd(ch, data)
        cmd.wave_point_cnt = len(data)
        self.s.send(cmd.build())

    def send_waveform_file(self, path: str, ch: int):
        """
        发送波形二进制文件
        :param path:文件路径
        :param ch:通道
        :return:返回执行状态
        """
        fd = open(path, 'rb')
        self.s.send(np.fromfile(fd, np.uint8))
        return self.get_ack_status()

    def send_waveform_data(self, data, ch: int):
        """
        波形数据下发
        :param data:下发数据
        :param ch:通道1-8
        :return:返回执行状态
        """
        yushu = len(data) % 16
        if yushu:
            cha = 16 - yushu
            a = np.zeros(cha, dtype=np.int8)
            data = np.append(data, a)
        array = np.asarray(data).clip(-1, 1)
        point = data * (2 ** 15 - 1)
        u16point = np.asarray(point, dtype=np.uint16).byteswap()
        self.send_wave(u16point, ch)
        return self.get_ack_status()

    def set_trigger_param(self, ch: int, trig_ch: int, trig_delay: int, mark_delay: int):
        """
        设置触发参数
        :param ch:通道
        :param trig_ch:触发通道
        :param trig_delay:触发延时
        :param mark_delay:
        :return: 返回指令执行结果
        """
        cmd = tcp_ch_tiggerselect_cmd()
        cmd.ch = ch
        cmd.ch_trigger = trig_ch
        zheng = trig_delay // 8
        yu = trig_delay % 8
        cmd.trigger_delay_cu = zheng
        cmd.trigger_delay_xi = yu
        cmd.markout_delay = mark_delay
        self.s.send(cmd.build())
        return self.get_ack_status()

    def set_fan_speed(self, speed: int):
        """
        设置风扇转速
        :param speed:转速区间0-400
        :return:
        """
        assert 0 <= speed <= 400, 'input speed error[0, 400]'

        cmd = tcp_fan_ctrl_cmd()
        cmd.speed = speed
        self.s.send(cmd.build())
        return self.get_ack_status()

    def get_temperature(self):
        """
        获取设备温度
        :return: 返回4组温度值
        """
        cmd = tcp_get_temp_cmd()
        self.s.send(cmd.build())
        msg = self.s.recv(24)
        a, b, c, t1, t2, t3, t4, d, e = struct.unpack('IBBHHHH6sI', msg)

        t5 = ((t1 >> 8) & 0xff) | ((t1 & 0xff) << 8)
        t6 = ((t2 >> 8) & 0xff) | ((t2 & 0xff) << 8)
        t7 = ((t3 >> 8) & 0xff) | ((t3 & 0xff) << 8)
        t8 = ((t4 >> 8) & 0xff) | ((t4 & 0xff) << 8)

        temp1 = t5 * 503 / pow(2, 16) - 273
        temp2 = t6 * 503 / pow(2, 16) - 273
        temp3 = t7 * 503 / pow(2, 16) - 273
        temp4 = t8 * 503 / pow(2, 16) - 273
        # print(f'{temp1} {temp2} {temp3} {temp4}')
        list = [temp1, temp2, temp3, temp4]
        return list

    def set_output_mode(self, ch: int, mode: str):
        """
        设置前端输出模式
        :param ch:通道
        :param mode:”AC“:AC模式输出 ”DC“:DC模式输出
        :return:
        """
        cmd = tcp_output_mode_cmd(ch, mode)
        self.s.send(cmd.build())
        return self.get_ack_status()

    def set_rf_power(self, ch: int, power: int):
        """
        设置衰减
        :param ch:通道
        :param power:衰减0-31dB
        :return:
        """
        assert 0 <= power <= 31, 'input power error[0, 31]'
        cmd = tcp_attenuation_cmd(ch, power)
        self.s.send(cmd.build())
        return self.get_ack_status()

    def set_data_source(self, freq: int, source: int):
        """
        设置数据源
        :param freq:输出频率MHz
        :param source:0:波形下载，通过trig播放
                      1:无需下载自行产生freq
                      2:无需trig,反复输出下载的波形
        :return:
        """
        if source == 1:
            fs_w = round(freq / 300 * pow(2, 16) / 8)
        else:
            fs_w = 0
        cmd = tcp_data_source_cmd(fs_w, source)
        self.s.send(cmd.build())
        return self.get_ack_status()
