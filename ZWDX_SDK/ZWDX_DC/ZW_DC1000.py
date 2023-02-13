import struct
import serial
import numpy as np
import socket
from enum import Enum


class ZW_STATUS(Enum):
    DISENABLE = 0
    ENABLE = 1
    OPEN = 2
    CLOSE = 3
    SUCCESS = 4
    FAIL = 5


class ZW_CH(Enum):
    CH1 = 0x0001
    CH2 = 0x0002
    CH3 = 0x0004
    CH4 = 0x0008
    CH5 = 0x0010
    CH6 = 0x0020
    CH7 = 0x0040
    CH8 = 0x0080
    CH9 = 0x0100
    CH10 = 0x0200
    CH11 = 0x0400
    CH12 = 0x0800
    CH13 = 0x1000
    CH14 = 0x2000
    CH15 = 0x4000
    CH16 = 0x8000
    CHALL = 0xFFFF


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


class reset_slope_cmd(cmd_base):
    hd = 0x55
    id = 0x01
    length = 8
    type = 0x10
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


class get_vol_cmd(cmd_base):
    hd = 0x55
    id = 0x01
    length = 8
    type = 0x0F
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


class get_vol_dac_cmd(cmd_base):
    hd = 0x55
    id = 0x01
    length = 8
    type = 0x11
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


class DC1000:
    connect_mode = None
    default_device_info = {'ip': '192.168.1.20', 'port': 8080}

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
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, True)
        self.s.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 60 * 1000, 10 * 1000))
        self.s.connect((ip, port))
        self.s.settimeout(50)
        self.connect_mode = "ethernet"
        status = self.init()
        return status

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
        status = self.init()
        return status

    def init(self):
        # 默认浮地模式
        status = self.control_gnd()
        return status

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

    def get_status(self):
        msg = self.zwdx_recv(7)
        format_str = '!BBBBBBB'
        a, b, c, d, status, e, f = struct.unpack(format_str, msg)
        return status

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
        """
        if vol > 10 or vol < -10:
            return

        cmd = vol_cmd()
        for i in range(1, 9, 1):
            if ch.value == (1 << (i - 1)):
                cmd.ch = i + 8
        b = format(vol, '.6f').encode('utf-8')
        length = len(b)
        cmd.vol.clear()
        for i in range(8):
            if i < length:
                cmd.vol.append(b[i])
            else:
                cmd.vol.append(0)

        self.zwdx_send(cmd.create_pack())
        return self.get_status()

    def get_vol(self, ch: ZW_CH):
        """
        获取电压值
        :param ch:ZW_CH1-ZW_CH8
        :return: 返回电压值 单位A
        """
        assert ZW_CH.CH1 <= ch.value <= ZW_CH.CH8, "input param error,please check."
        cmd = get_vol_cmd()
        status = None
        rtn_vol = None
        for i in range(1, 9, 1):
            if ch == (1 << (i - 1)):
                cmd.ch = i + 8
                self.zwdx_send(cmd.create_pack())
                msg = self.zwdx_recv(11)
                a, b, c, d, e, vol, f, g = struct.unpack('!BBBBBIBB', msg)
                print('code = %#x' % vol)
                rtn_vol = round(vol * 20 / 0xFFFFF - 10, 6)
        return rtn_vol

    def get_vol_dac(self, ch: ZW_CH):
        """
        获取电压值
        :param ch:ZW_CH.CH[1-8]
        :return: 返回电压值 单位V
        """
        assert ZW_CH.CH1 <= ch.value <= ZW_CH.CH8, "input param error,please check."
        cmd = get_vol_dac_cmd()
        status = None
        rtn_vol = None
        for i in range(1, 9, 1):
            if ch == (1 << (i - 1)):
                cmd.ch = i + 8
                self.zwdx_send(cmd.create_pack())
                msg = self.zwdx_recv(11)
                a, b, c, d, e, vol, f, g = struct.unpack('!BBBBBIBB', msg)
                print('code = %#x' % vol)
                rtn_vol = round(vol * 20 / 0xFFFFF - 10, 6)
        return rtn_vol

    def set_volt_slope(self, slope):
        """
        设置上升或下降的斜率
        :param slope:单位mv/s.默认1000mv/s
        """
        cmd = slope_cmd()
        cmd.slope = slope
        self.zwdx_send(cmd.create_pack())
        status = self.get_status()
        return status

    def _open_ch(self, ch, mode):
        """
        打开单个通道
        :param ch:
        :param mode: 1：安全打开 2：安全关闭 3：快速打开 4：快速关闭
        :return:
        """
        cmd = open_close_cmd()
        cmd.switch = mode
        status = None
        for i in range(1, 9, 1):
            if ch == (1 << (i - 1)):
                cmd.ch = i + 8
                self.zwdx_send(cmd.create_pack())
                status = self.get_status()
        return status

    def _close_ch(self, ch, mode):
        cmd = open_close_cmd()
        cmd.switch = mode
        status = None
        for i in range(1, 9, 1):
            if ch == (1 << (i - 1)):
                cmd.ch = i + 8
                self.zwdx_send(cmd.create_pack())
                status = self.get_status()
        return status

    def set_ch_status(self, ch: ZW_CH, st: ZW_STATUS):
        """
        安全打开或关闭通道
        :param ch:ZW_ENUM.CH1-CH8
        :param st:ZW_ENUM.OPEN: 打开 ZW_ENUM.CLOSE: 关闭
        :return:返回执行结果 0xFF:表示成功
        """
        assert ZW_CH.CH1.value <= ch.value <= ZW_CH.CH8.value, "input param error,please check."
        status = None
        for i in ZW_CH:
            if ch == i:
                if st == ZW_STATUS.OPEN:
                    status = self._open_ch(i.value, 1)
                else:
                    status = self._close_ch(i.value, 2)
        return status

    def set_ch_status_fast(self, ch: ZW_CH, st: ZW_STATUS):
        """
        快速打开或关闭通道
        :param ch:ZW_ENUM.CH[1-8]
        :param st:ZW_ENUM.OPEN: 打开 ZW_ENUM.CLOSE: 关闭
        :return:返回执行结果 0xFF:表示成功
        """
        assert ZW_CH.CH1.value <= ch.value <= ZW_CH.CH8.value, "input param error,please check."
        status = None
        for i in ZW_CH:
            if ch == i:
                if st == ZW_STATUS.OPEN:
                    status = self._open_ch(i.value, 3)
                else:
                    status = self._close_ch(i.value, 4)
        return status

    def get_current(self, ch: ZW_CH):
        """
        获取通道电流
        :param ch: ZW_DC1000.CH[1-8]
        :return: 单位A
        """
        assert ZW_CH.CH1.value <= ch.value <= ZW_CH.CH8.value, "input param error,please check."
        cmd = current_cmd()
        for i in range(1, 9, 1):
            if ch.value == (1 << (i - 1)):
                cmd.ch = i
        self.zwdx_send(cmd.create_pack())
        msg = self.zwdx_recv(11)
        a, b, c, d, e, current, f, g = struct.unpack('!BBBBBiBB', msg)

        return current / 1000 / 1000 / 1000 / 1000

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
        return self.get_status()

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
        if st == ZW_STATUS.ENABLE:
            cmd.st = 1
        else:
            cmd.st = 0
        self.zwdx_send(cmd.create_pack())
        return self.get_status()

    def res_term(self, ch: ZW_CH, val: ZW_STATUS):
        """
        设置某个通道端接电阻1MΩ使能
        :param ch:通道1-8
        :param val: 使能：ZW_STATUS.ENABLE 不使能：ZW_STATUS.DISENABLE
        :return:状态信号
        """
        assert ZW_CH.CH1.value <= ch.value <= ZW_CH.CH8.value, "input param error,please check."
        status = None
        for i in range(1, 9, 1):
            if ch.value == (1 << (i - 1)):
                status = self.set_dis(i - 1, 0, val)
        return status

    def cap_term(self, ch: ZW_CH, val: ZW_STATUS):
        """
        设置某个通道端接电容1uF使能
        :param ch:ZW_CH[1-8]
        :param val: 使能：ZW_STATUS.ENABLE 不使能：ZW_STATUS.DISENABLE
        :return:状态信号
        """
        assert ZW_CH.CH1.value <= ch.value <= ZW_CH.CH8.value, "input param error,please check."
        status = None
        for i in range(1, 9, 1):
            if ch.value == (1 << (i - 1)):
                status = self.set_dis(i - 1, 1, val)
        return status

    def iv_term(self, ch: ZW_CH, val: ZW_STATUS):
        """
        设置某个通道电流采集功能
        :param ch:ZW_CH[1-8]
        :param val: 使能：ZW_STATUS.ENABLE 不使能：ZW_STATUS.DISENABLE
        :return:状态信号
        """
        assert ZW_CH.CH1.value <= ch.value <= ZW_CH.CH8.value, "input param error,please check."
        status = None
        for i in range(1, 9, 1):
            if ch.value == (1 << (i - 1)):
                status = self.set_dis(i - 1, 2, val)
        return status

    def _set_pwm_status(self, ch: ZW_CH, val: ZW_STATUS):
        """
        使能PWM调节2uv精度，内部测试使用
        :param ch:ZW_CH[1-8]
        :param val:使能：ZW_STATUS.ENABLE 不使能：ZW_STATUS.DISENABLE
        :return: 状态信号0xFF
        """
        assert ZW_CH.CH1.value <= ch.value <= ZW_CH.CH8.value, "input param error,please check."
        status = self.set_dis(ch - 1, 3, val)
        return status

    def _set_reset_slop(self, slop):
        """
        设置设备后面复位按钮下降斜率，内部测试使用
        :param slop:斜率mv/s
        :return: 执行结果 0xFF:成功
        """
        cmd = reset_slope_cmd()
        cmd.slope = slop
        self.zwdx_send(cmd.create_pack())
        return self.get_status()
