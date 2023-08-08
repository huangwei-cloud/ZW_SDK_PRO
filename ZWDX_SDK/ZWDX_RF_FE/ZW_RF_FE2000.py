import socket
import struct
import numpy as np
from enum import Enum


class cmd_base:
    head = 0xF7F6F5F4
    cmd = np.uint32(0)
    len = 0x00020000  # 512

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


class get_set_device_info_cmd(cmd_base):
    hd = 0x55
    id = 0x00
    length = 0x5B
    type = 0x00  # 0xFE获取设备信息 0xFF保存设备信息
    info = []

    def create_pack(self):
        buffer = [self.hd, self.id, self.length, self.type]
        buffer += self.info
        super().set_cmd(buffer)
        return super().build()


class XY_CH(Enum):
    # B_XY1_1 = 0
    # B_XY2_1 = 1
    # B_XY3_1 = 2
    # B_XY4_1 = 3
    # B_XY1_2 = 4
    # B_XY2_2 = 5
    # B_XY3_2 = 6
    # B_XY4_2 = 7
    B_XY1_1 = 0
    B_XY1_2 = 1
    B_XY2_1 = 2
    B_XY2_2 = 3
    B_XY3_1 = 4
    B_XY3_2 = 5
    B_XY4_1 = 6
    B_XY4_2 = 7


# class QA_CH(Enum):
#     OUT1 = 0  # PCIE Card1 "OUT" connect to "B_IN1"
#     IN1 = 0  # PCIE Card1 "In" connect to "B_OUT1"
#     OUT2 = 1  # PCIE Card2 "OUT" connect to "B_IN2"
#     IN2 = 1  # PCIE Card2 "In" connect to "B_OUT2"


class PI_CH(Enum):
    B_IN1 = 0
    B_IN2 = 1


class RO_CH(Enum):
    B_OUT1 = 0
    B_OUT2 = 1


class RF_FE2000:

    default_device_info = {"ip": "192.168.1.XXX", "port": 8080}

    def __init__(self):
        self.s = None

    def __def__(self):
        if self.s is not None:
            self.s.close()

    def ethernet_connect(self, ip: str, port: int):
        """
        以太网方式连接设备
        :param ip: ip地址默认192.168.1.XXX
        :param port: 端口，默认8080
        :return:
        """

        assert 1 <= port <= 65535, 'input param error,please check[1,65535]'
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, True)
        self.s.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 60 * 1000, 10 * 1000))
        self.s.connect((ip, port))
        self.s.settimeout(50)
        return True

    def set_ip_mask(self, ip='', mask='255.255.255.0', gw='192.168.0.1'):
        """
        改变设备IP
        :param ip: 设备IP
        :param mask:子网掩码
        :param gw: 网关
        """
        ip_list = []
        mask_list = []
        gw_list = []
        ip_list = ip.split('.')
        int_ip_list = list(map(int, ip_list))
        mask_list = mask.split('.')
        int_mask_list = list(map(int, mask_list))
        gw_list = gw.split('.')
        int_gw_list = list(map(int, gw_list))

        get_cmd = get_set_device_info_cmd()
        get_cmd.type = 0xFE
        self.s.send(get_cmd.create_pack())
        msg = self.s.recv(88)
        nparr = np.frombuffer(msg, np.uint8).copy()
        nparr[74:78] = int_ip_list
        nparr[80:84] = int_mask_list
        nparr[84:88] = int_gw_list
        set_cmd = get_set_device_info_cmd()
        set_cmd.type = 0xFF
        set_cmd.info = nparr.tolist()
        self.s.send(set_cmd.create_pack())

    def set_xy_att(self, ch, db):
        """
        PCIE Card1 "XY-1/2/3/4" connect to "B_XY1/2/3/4_1"
        CH:Freq is 4.2-5.5GHz, GAIN is ≈5dB, the default attenuation is 30dB.
        :param ch:XY_CH
        :param db:
        :return:
        """
        att = round(db // 0.25)
        frame = struct.pack("BBBBBB", 0xAA, 0x01, ch.value, att, (0x01+ch.value+att) & 0xff, 0x55)
        self.s.send(frame)
        self.s.recv(6)

    def get_xy_att(self, ch):
        frame = struct.pack("BBBBBB", 0xAA, 0x81, ch.value, 0, (0x81 + ch.value + 0) & 0xff, 0x55)
        self.s.send(frame)
        msg = self.s.recv(6)
        buffer = np.frombuffer(msg, np.uint8)
        return buffer[3] * 0.25

    def set_in_att(self, ch, db):
        """
        PCIE Card1 "OUT" connect to "B_IN1"
        CH:Freq is 6.2-7.5GHz, GAIN is ≈5dB, the default attenuation is 30dB.
        :param ch:PI_CH
        :param db:
        :return:
        """
        att = round(db // 0.25)
        frame = struct.pack("BBBBBB", 0xAA, 0x02, ch.value, att, (0x02 + ch.value + att) & 0xff, 0x55)
        self.s.send(frame)
        self.s.recv(6)

    def get_in_att(self, ch):
        frame = struct.pack("BBBBBB", 0xAA, 0x82, ch.value, 0, (0x82 + ch.value + 0) & 0xff, 0x55)
        self.s.send(frame)
        msg = self.s.recv(6)
        buffer = np.frombuffer(msg, np.uint8)
        return buffer[3] * 0.25

    def set_out_att(self, ch, db):
        att = round(db // 0.25)
        frame = struct.pack("BBBBBB", 0xAA, 0x03, ch.value, att, (0x03 + ch.value + att) & 0xff, 0x55)
        self.s.send(frame)
        self.s.recv(6)

    def get_out_att(self, ch):
        """
        PCIE Card1 "In" connect to "B_OUT1"
        CH:Freq is 6.2-7.5GHz, GAIN is ≈55dB, the default attenuation is 60dB.
        :param ch:RO_CH
        :return:
        """
        frame = struct.pack("BBBBBB", 0xAA, 0x83, ch.value, 0, (0x83 + ch.value + 0) & 0xff, 0x55)
        self.s.send(frame)
        msg = self.s.recv(6)
        buffer = np.frombuffer(msg, np.uint8)
        return buffer[3] * 0.25



