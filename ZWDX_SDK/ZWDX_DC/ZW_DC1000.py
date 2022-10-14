import sys
import time
import struct
import serial
import numpy as np
from socket import socket, AF_INET, SOCK_STREAM


g_vol_dic = {
    "ch1": 0,
    "ch2": 0,
    "ch3": 0,
    "ch4": 0,
    "ch5": 0,
    "ch6": 0,
    "ch7": 0,
    "ch8": 0,
}


class cmd_base:
    head = 0xF7F6F5F4
    cmd = np.uint32(0)
    len = np.uint32(524)

    ad_da_cmd = []

    zero = []

    def __init__(self):
        pass

    def build(self):
        format_str = '!3I' + str(len(self.ad_da_cmd)) + 's'
        self.zero.clear()
        for i in range(524 - len(self.ad_da_cmd) - 12):
            self.zero.append(0)
        send_str = struct.pack(format_str, self.head, self.cmd, self.len,
                               np.asarray(self.ad_da_cmd, np.uint8).tobytes())
        send_str += np.asarray(self.zero, np.uint8).tobytes()
        return send_str

    def set_cmd(self, cmd_list=None):
        self.ad_da_cmd.clear()
        self.ad_da_cmd += cmd_list


class vol_cmd(cmd_base):
    hd = 0x55
    id = 0x01
    length = 8
    type = 0x01
    ch = None
    vol = []
    crc = 0
    end = 0xaa

    def __init__(self):
        super().__init__()
        pass

    def create_pack(self):
        buffer = [self.hd, self.id, self.length, self.type, self.ch]
        buffer += self.vol
        buffer.append(self.crc)
        buffer.append(self.end)
        super().set_cmd(buffer)
        return super().build()


class slope_cmd(cmd_base):
    hd = 0x55
    id = 0x01
    length = 8
    type = 0x03
    slope = 0x00000000
    crc = 0
    end = 0xaa

    def __init__(self):
        super().__init__()
        pass

    def create_pack(self):
        buffer = [self.hd, self.id, self.length, self.type, self.slope & 0xff, (self.slope >> 8) & 0xff,
                  (self.slope >> 16) & 0xff, (self.slope >> 24) & 0xff, self.crc, self.end]
        super().set_cmd(buffer)
        return super().build()


class open_close_cmd(cmd_base):
    hd = 0x55
    id = 0x01
    length = 8
    type = 0x02
    ch = 0x00
    switch = 0x00
    crc = 0
    end = 0xaa

    def __init__(self):
        super().__init__()
        pass

    def create_pack(self):
        buffer = [self.hd, self.id, self.length, self.type, self.ch, self.switch, self.crc, self.end]
        super().set_cmd(buffer)
        return super().build()


class current_cmd(cmd_base):
    hd = 0x55
    id = 0x01
    length = 8
    type = 0x04
    ch = 0x00
    crc = 0
    end = 0xaa

    def __init__(self):
        super().__init__()
        pass

    def create_pack(self):
        buffer = [self.hd, self.id, self.length, self.type, self.ch, self.crc, self.end]
        super().set_cmd(buffer)
        return super().build()


class led_cmd(cmd_base):
    hd = 0x55
    id = 0x01
    length = 8
    type = 0x05
    ch = 0x00
    status = 0
    crc = 0
    end = 0xaa

    def __init__(self):
        super().__init__()
        pass

    def create_pack(self):
        buffer = [self.hd, self.id, self.length, self.type, self.ch, self.status, self.crc, self.end]
        super().set_cmd(buffer)
        return super().build()


class gnd_cmd(cmd_base):
    hd = 0x55
    id = 0x01
    length = 8
    type = 0x06
    ch = 0x00
    status = 0
    crc = 0
    end = 0xaa

    def __init__(self):
        super().__init__()
        pass

    def create_pack(self):
        buffer = [self.hd, self.id, self.length, self.type, self.ch, self.status, self.crc, self.end]
        super().set_cmd(buffer)
        return super().build()


class dev_id_cmd(cmd_base):
    hd = 0x55
    id = 0x01
    length = 8
    type = 0x07
    dev_id = 0
    crc = 0
    end = 0xaa

    def __init__(self):
        super().__init__()
        pass

    def create_pack(self):
        buffer = [self.hd, self.id, self.length, self.type, self.dev_id, self.crc, self.end]
        super().set_cmd(buffer)
        return super().build()


class ip_cmd(cmd_base):
    hd = 0x55
    id = 0x01
    length = 11
    type = 0x08
    ip = []
    mask = []
    crc = 0
    end = 0xaa

    def __init__(self, ip=[], mask=[]):
        super().__init__()
        self.ip = ip
        self.mask = mask

    def create_pack(self):
        buffer = [self.hd, self.id, self.length, self.type]
        buffer += self.ip
        buffer += self.mask
        buffer.append(self.crc)
        buffer.append(self.end)

        super().set_cmd(buffer)

        return super().build()


class verify_cmd(cmd_base):
    hd = 0x55
    id = 0x01
    length = 8
    type = 0x09
    ch = 0
    k_str = []
    b_str = []
    crc = 0
    end = 0xaa

    def __init__(self):
        super().__init__()
        pass

    def create_pack(self):
        buffer = [self.hd, self.id, self.length, self.type, self.ch]
        buffer += self.k_str
        buffer += self.b_str
        buffer.append(self.crc)
        buffer.append(self.end)
        super().set_cmd(buffer)
        return super().build()


class status_cmd(cmd_base):
    hd = 0x55
    id = 0x01
    length = 8
    type = 0x0a
    crc = 0
    end = 0xaa

    def __init__(self):
        super().__init__()
        pass

    def create_pack(self):
        buffer = [self.hd, self.id, self.length, self.type, self.crc, self.end]
        super().set_cmd(buffer)
        return super().build()


class heartbeat_cmd(cmd_base):
    hd = 0x55
    id = 0x01
    length = 6
    type = 0x0B
    heart = [ord('Z'), ord('W'), ord('D'), ord('X')]
    crc = 0
    end = 0xaa

    def __init__(self):
        super().__init__()
        pass

    def create_pack(self):
        buffer = []
        buffer += [self.hd, self.id, self.length, self.type]
        buffer += self.heart
        buffer += [self.crc, self.end]
        super().set_cmd(buffer)
        return super().build()


class dycode_cmd(cmd_base):
    hd = 0x55
    id = 0x01
    length = 8
    type = 0x0C
    ch = 1
    dycode = 0x00000000
    crc = 0
    end = 0xaa

    def __init__(self):
        super().__init__()
        pass

    def create_pack(self):
        buffer = []
        buffer += [self.hd, self.id, self.length, self.type, self.ch]
        buffer += [self.dycode & 0xFF, (self.dycode >> 8) & 0xFF, (self.dycode >> 16) & 0xFF,
                   (self.dycode >> 24) & 0xFF]
        buffer += [self.crc, self.end]
        super().set_cmd(buffer)
        return super().build()


class pwm_set_cmd(cmd_base):
    hd = 0x55
    id = 0x01
    length = 8
    type = 0x0D
    ch = 0
    t = None
    level = None
    crc = 0
    end = 0xaa

    def __init__(self):
        super().__init__()
        pass

    def create_pack(self):
        buffer = []
        buffer += [self.hd, self.id, self.length, self.type, self.ch]
        buffer += [self.t & 0xFF, (self.t >> 8) & 0xFF, (self.t >> 16) & 0xFF, (self.t >> 24) & 0xFF,
                   (self.t >> 32) & 0xFF, (self.t >> 40) & 0xFF, (self.t >> 48) & 0xFF, (self.t >> 56) & 0xFF]
        buffer += [self.level & 0xFF, (self.level >> 8) & 0xFF, (self.level >> 16) & 0xFF, (self.level >> 24) & 0xFF,
                   (self.level >> 32) & 0xFF, (self.level >> 40) & 0xFF, (self.level >> 48) & 0xFF,
                   (self.level >> 56) & 0xFF]
        buffer += [self.crc, self.end]
        super().set_cmd(buffer)
        return super().build()


class set_ch_dis(cmd_base):
    hd = 0x55
    id = 0x01
    length = 8
    type = 0x0E
    ch = 0
    ty = 0
    st = 0
    crc = 0
    end = 0xaa

    def __init__(self):
        super().__init__()
        pass

    def create_pack(self):
        buffer = []
        buffer += [self.hd, self.id, self.length, self.type]
        buffer += [self.ch, self.ty, self.st]
        buffer += [self.crc, self.end]
        super().set_cmd(buffer)
        return super().build()


class DC1000:
    ch_status_dic = {'1': False, '2': False, '3': False, '4': False, '5': False,
                     '6': False, '7': False, '8': False}
    connect_mode = None
    default_device_info = {'ip': '192.168.1.20', 'port': 8080}

    # 解决电压改变后第一次读取电流总是上一次电流的问题
    ch_last_vol = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0}
    ch_current_vol = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0}

    def __init__(self):
        self.s = None

    def __del__(self):
        if self.s is not None:
            self.s.close()

    def ethernet_connect(self, ip: str, port: int):
        """
        以太网方式连接设备
        :param ip: ip地址默认192.168.1.20
        :param port: 端口，默认8080
        :return:
        """
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.connect((ip, port))
        self.s.settimeout(10)
        self.connect_mode = "ethernet"
        self.init()

    def uart_connect(self, com: str):
        """
        串口方式连接设备
        :param com: 串口号，大写"COM3"
        :return:
        """
        try:
            self.s = serial.Serial(com, 115200, stopbits=1, bytesize=8, parity='N', timeout=10)
        except serial.SerialException:
            print("Is com port being used by other application?")
        self.connect_mode = "uart"
        self.init()

    def init(self):
        # 默认浮地模式
        self.control_gnd()

    def zwdx_send(self, data):
        if self.connect_mode == "ethernet":
            self.s.send(data)
        else:
            self.s.write(data)

    def zwdx_recv(self, length):
        msg = None
        if self.connect_mode == "ethernet":
            msg = self.s.recv(length)
        else:
            msg = self.s.read(length)
        return msg

    def check_device_status(self):
        """
        使用心跳包检测设备是否处于在线状态
        :return: True: online   False:offline
        """
        self.zwdx_send(heartbeat_cmd().create_pack())
        try:
            msg = self.zwdx_recv(10)
            return True
        except Exception as e:
            print(f'心跳回复超时,设备断开连接,请检查设备......')
            return False

    def _check_status(self, ch=1):
        """
        检测通道开启状态
        :param ch:通道1-8
        :return: True:open False: off
        """
        if not self.ch_status_dic[str(ch)]:
            print(f'please open ch{ch}')
            return False
        return True

    def set_dy_code(self, ch=1, dycode=0x7FFFF):
        """
        内部测试使用接口
        :param ch:
        :param dycode:
        :return:
        """
        cmd = dycode_cmd()
        cmd.ch = ch + 8
        cmd.dycode = dycode
        self.zwdx_send(cmd.create_pack())

    def change_ip(self, ip='', mask='255.255.255.0'):
        """
        改变设备IP
        :param ip: 设备IP
        :param mask:
        :return:
        """
        ip_list = []
        mask_list = []
        ip_list = ip.split('.')
        int_ip_list = list(map(int, ip_list))
        mask_list = mask.split('.')
        int_mask_list = list(map(int, mask_list))
        cmd = ip_cmd(int_ip_list, int_mask_list)

        self.zwdx_send(cmd.create_pack())

    def set_pwm_set(self, ch, t, level):
        """
        内部测试接口
        :param level:高电平
        :param t: 周期
        :param ch: 通道
        :return:
        """
        cmd = pwm_set_cmd()
        cmd.ch = ch
        cmd.t = t
        cmd.level = level
        self.zwdx_send(cmd.create_pack())

    def set_vol(self, ch, vol):
        """
        设置DA输出电压
        :param ch: 1-8
        :param vol: 电压值[-10, 10]V
        :return:
        """
        if vol > 10 or vol < -10:
            return

        cmd = vol_cmd()
        # 实际通道号要偏移8
        cmd.ch = ch + 8
        b = format(vol, '.6f').encode('utf-8')
        length = len(b)
        cmd.vol.clear()
        for i in range(8):
            if i < length:
                cmd.vol.append(b[i])
            else:
                cmd.vol.append(0)

        self.zwdx_send(cmd.create_pack())
        global g_vol_dic
        g_vol_dic['ch' + str(ch)] = vol
        self.ch_current_vol[str(ch)] = vol

    def set_slope(self, slope):
        """
        设置上升或下降的斜率
        :param slope:单位mv/s.默认1000mv/s
        :return:
        """
        cmd = slope_cmd()
        cmd.slope = slope
        self.zwdx_send(cmd.create_pack())

    def open_ch(self, ch):
        """
        打开通道
        :param ch:1-8
        :return:
        """
        assert 1 <= ch <= 8, "please check channel value[1-8]"
        cmd = open_close_cmd()
        cmd.ch = ch + 8
        cmd.switch = 0x02
        self.zwdx_send(cmd.create_pack())
        self.ch_status_dic[str(ch)] = True

    def close_ch(self, ch):
        assert 1 <= ch <= 8, "please check channel value[1-8]"
        cmd = open_close_cmd()
        cmd.ch = ch + 8
        cmd.switch = 0x01
        self.zwdx_send(cmd.create_pack())
        global g_vol_dic
        g_vol_dic['ch' + str(ch)] = 0
        self.ch_status_dic[str(ch)] = False

    def get_current(self, ch):
        """
        获取通道电流
        :param ch: 通道1-8
        :return: 单位A
        """
        assert 1 <= ch <= 8, "please check channel value[1-8]"
        cmd = current_cmd()
        cmd.ch = ch
        format_str = '!BBBBBiBB'
        current_pa = None

        if self.ch_current_vol[str(ch)] == self.ch_last_vol[str(ch)]:
            self.zwdx_send(cmd.create_pack())
            msg = self.zwdx_recv(11)
            a, b, c, d, e, current, f, g = struct.unpack(format_str, msg)
            current_pa = current
        else:  # 电压改变后，第一次获取电流不要
            self.zwdx_send(cmd.create_pack())
            msg = self.zwdx_recv(11)
            # 第二次电流作为有效值返回
            self.zwdx_send(cmd.create_pack())
            msg = self.zwdx_recv(11)
            a, b, c, d, e, current, f, g = struct.unpack(format_str, msg)
            current_pa = current
            self.ch_last_vol[str(ch)] = self.ch_current_vol[str(ch)]
        return current_pa / 1000 / 1000 / 1000 / 1000

    def control_gnd(self, status='FLOAT_GND'):
        """
        设置仪器模式，内部测试使用
        :param status: "COMMON_GND":共地  “FLOAT_GND”：浮地
        :return:
        """
        cmd = gnd_cmd()
        cmd.ch = 9
        if status == 'COMMON_GND':
            cmd.status = 1
        elif status == 'FLOAT_GND':
            cmd.status = 0
        else:
            print("input str error")
        self.zwdx_send(cmd.create_pack())

    def set_verify_code(self, ch, k, b):
        """
        设置各通道校验码，内部测试使用
        y = kx + b
        :param ch:通道1-8
        :param k:斜率，默认：1
        :param b:轴便移，默认0
        :return:
        """
        cmd = verify_cmd()
        cmd.ch = ch
        k_str = str(k).encode('utf-8')
        b_str = str(b).encode('utf-8')
        k_len = len(k_str)
        b_len = len(b_str)
        cmd.k_str.clear()
        cmd.b_str.clear()
        for i in range(8):
            if i < k_len:
                cmd.k_str.append(k_str[i])
            else:
                cmd.k_str.append(0)

        for i in range(8):
            if i < b_len:
                cmd.b_str.append(b_str[i])
            else:
                cmd.b_str.append(0)
        self.zwdx_send(cmd.create_pack())

    def set_dis(self, ch, type, st):
        cmd = set_ch_dis()
        cmd.ch = ch
        cmd.ty = type
        cmd.st = st
        self.zwdx_send(cmd.create_pack())

    def R_TERM(self, ch, val=0):
        """
        设置某个通道端接电阻1MΩ使能
        :param ch:通道1-8
        :param val: 0：不使能 1：使能
        :return:
        """
        assert 1 <= ch <= 8, "please check channel value[1-8]"
        self.set_dis(ch - 1, 0, val)

    def C_TERM(self, ch, val=0):
        """
        设置某个通道端接电容1uF使能
        :param ch:
        :param val: 0：不使能 1：使能
        :return:
        """
        assert 1 <= ch <= 8, "please check channel value[1-8]"
        self.set_dis(ch - 1, 1, val)

    def IVDIS(self, ch, val=0):
        """
        设置某个通道电流采集功能
        :param ch:通道1-8
        :param val: 0：不使能 1：使能
        :return:
        """
        assert 1 <= ch <= 8, "please check channel value[1-8]"
        self.set_dis(ch - 1, 2, val)

