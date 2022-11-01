import numpy as np
import struct
import time
import serial
from socket import socket, AF_INET, SOCK_STREAM
from enum import Enum

base_address = 0x43C0_0000


class axi_slv_reg_offset(Enum):
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG0_OFFSET = 0
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG1_OFFSET = 4
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG2_OFFSET = 8
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG3_OFFSET = 12
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG4_OFFSET = 16
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG5_OFFSET = 20
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG6_OFFSET = 24
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG7_OFFSET = 28
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG8_OFFSET = 32
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG9_OFFSET = 36
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG10_OFFSET = 40
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG11_OFFSET = 44  # 开关
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG12_OFFSET = 48
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG13_OFFSET = 52
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG14_OFFSET = 56
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG15_OFFSET = 60
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG16_OFFSET = 64
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG17_OFFSET = 68
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG18_OFFSET = 72
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG19_OFFSET = 76
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG20_OFFSET = 80
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG21_OFFSET = 84
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG22_OFFSET = 88
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG23_OFFSET = 92
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG24_OFFSET = 96
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG25_OFFSET = 100
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG26_OFFSET = 104
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG27_OFFSET = 108
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG28_OFFSET = 112
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG29_OFFSET = 116
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG30_OFFSET = 120
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG31_OFFSET = 124
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG32_OFFSET = 128
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG33_OFFSET = 132
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG34_OFFSET = 136
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG35_OFFSET = 140
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG36_OFFSET = 144
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG37_OFFSET = 148
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG38_OFFSET = 152
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG39_OFFSET = 156
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG40_OFFSET = 160
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG41_OFFSET = 164
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG42_OFFSET = 168
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG43_OFFSET = 172
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG44_OFFSET = 176
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG45_OFFSET = 180
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG46_OFFSET = 184
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG47_OFFSET = 188
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG48_OFFSET = 192
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG49_OFFSET = 196
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG50_OFFSET = 200
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG51_OFFSET = 204
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG52_OFFSET = 208
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG53_OFFSET = 212
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG54_OFFSET = 216
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG55_OFFSET = 220
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG56_OFFSET = 224
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG57_OFFSET = 228
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG58_OFFSET = 232
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG59_OFFSET = 236
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG60_OFFSET = 240


class cmd_type(Enum):
    REG_SET_CMD = 0x01
    HEARTBEAT_CMD = 0x02


class cmd_base:
    head = 0xF7F6F5F4
    cmd = 0
    len = 524
    ad_da_cmd = []
    zero = []

    def __init__(self):
        pass

    def build(self):
        format_str = '!3I' + str(len(self.ad_da_cmd)) + 's'
        self.zero.clear()
        for i in range(524 - len(self.ad_da_cmd) - 12):
            self.zero.append(0)
        write_str = struct.pack(format_str, self.head, self.cmd, self.len,
                                np.asarray(self.ad_da_cmd, np.uint8).tobytes())
        write_str += np.asarray(self.zero, np.uint8).tobytes()
        return write_str


class set_reg_cmd(cmd_base):
    hd = 0x55
    id = 0x01
    length = 3
    type = cmd_type.REG_SET_CMD.value
    base_address = 0
    offset = 0
    reg = 0

    def __init__(self):
        super().__init__()

    def create_pack(self):
        self.ad_da_cmd = [self.hd, self.id, self.length, self.type, self.base_address & 0xff,
                          (self.base_address >> 8) & 0xff, (self.base_address >> 16) & 0xff,
                          (self.base_address >> 24) & 0xff,
                          (self.offset >> 0) & 0xff, (self.offset >> 8) & 0xff, (self.offset >> 16) & 0xff,
                          (self.offset >> 24) & 0xff,
                          (self.reg >> 0) & 0xff, (self.reg >> 8) & 0xff, (self.reg >> 16) & 0xff,
                          (self.reg >> 24) & 0xff]
        return self.build()


class heart_cmd(cmd_base):
    hd = 0x55
    id = 0x01
    length = 3
    type = cmd_type.HEARTBEAT_CMD.value
    heart = [ord('Z'), ord('W'), ord('D'), ord('X')]

    def __init__(self):
        super().__init__()

    def create_pack(self):
        self.ad_da_cmd = [self.hd, self.id, self.length, self.type]
        self.ad_da_cmd += self.heart
        return self.build()


class TMU1000:
    connect_mode = None

    def __init__(self):
        self.s = None

    def __del__(self):
        if self.s is not None:
            self.s.close()

    def ethernet_connect(self, ip: str, port: int):
        """
        以太网方式连接设备
        :param ip: ip地址默认192.168.1.110
        :param port: 端口，默认8080
        :return:
        """
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.connect((ip, port))
        self.s.settimeout(10)
        self.connect_mode = "ethernet"

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
        self.zwdx_send(heart_cmd().create_pack())
        try:
            msg = self.zwdx_recv(8)
            return True
        except Exception as e:
            print(f'心跳回复超时,设备断开连接,请检查设备......')
            return False

    def dev_mem(self, base, offset, data):
        cmd = set_reg_cmd()
        cmd.base_address = base_address
        cmd.offset = offset
        cmd.reg = data
        self.zwdx_send(cmd.create_pack())

    def set_trig_time(self, T):
        # assert fs_hz % 5 == 0, "error input, input is an integer multiple of 5"
        self.dev_mem(base_address, axi_slv_reg_offset.ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG0_OFFSET.value, T)

    def set_diff_trig_time(self, T):
        # assert fs_hz % 5 == 0, "error input, input is an integer multiple of 5"
        self.dev_mem(base_address, axi_slv_reg_offset.ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG60_OFFSET.value, T)

    def set_trig_delay(self, ch, value_ps):
        # assert 1 <= ch <= 10, "please check channel value[1-10]"
        for i in axi_slv_reg_offset:
            if i.value == ch * 4:
                self.dev_mem(base_address, i.value, value_ps)

    def set_diff_trig_delay(self, ch, value_ps):
        # assert 1 <= ch <= 10, "please check channel value[1-10]"
        for i in axi_slv_reg_offset:
            if i.value == (ch + 11) * 4:
                self.dev_mem(base_address, i.value, value_ps)

    def close_all_channels(self):
        self.dev_mem(base_address, axi_slv_reg_offset.ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG11_OFFSET.value, 0x0)

    def open_all_channels(self):
        self.dev_mem(base_address, axi_slv_reg_offset.ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG11_OFFSET.value, 0xFFFFFFFF)

    def set_refclk(self, ref: str):
        if ref == "int_ref":
            self.dev_mem(base_address, axi_slv_reg_offset.ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG60_OFFSET.value, 0)
        elif ref == "ext_ref":
            self.dev_mem(base_address, axi_slv_reg_offset.ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG60_OFFSET.value, 1)
        else:
            print(f"input param error...")

    def single_sync(self):
        self.set_trig_delay(1, 350)
        time.sleep(0.5)
        self.set_trig_delay(2, 160)
        time.sleep(0.5)
        self.set_trig_delay(3, 70)
        time.sleep(0.5)
        self.set_trig_delay(4, 200)
        time.sleep(0.5)
        self.set_trig_delay(5, 50)
        time.sleep(0.5)
        self.set_trig_delay(6, 80)
        time.sleep(0.5)
        self.set_trig_delay(7, 120)
        time.sleep(0.5)
        self.set_trig_delay(8, 0)
        time.sleep(0.5)
        self.set_trig_delay(9, 100)
        time.sleep(0.5)
        self.set_trig_delay(10, 950)

    def diff_sync(self):
        for i in range(1, 49, 1):
            self.set_diff_trig_delay(i, 0)

    def factory_reset(self):
        self.single_sync()
        self.diff_sync()
