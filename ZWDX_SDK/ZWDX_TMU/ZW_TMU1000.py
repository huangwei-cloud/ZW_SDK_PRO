import sys

import numpy as np
import struct
import time
import threading
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


class ZWDX_TMU(threading.Thread):
    def __init__(self):
        self.lock = threading.Lock()
        super().__init__()
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.connect(('192.168.1.108', 1008))
        self.s.settimeout(10)  # 设置超时错误

    def __del__(self):
        self.s.close()

    def run(self):
        while True:
            self.zwdx_send(heart_cmd().create_pack())
            try:
                msg = self.zwdx_recv()
            except Exception as e:
                print(f'心跳回复超时,设备断开连接,请检查设备......')
                self.s.close()
                connect_cnt = 0
                while True:
                    print('设备重连中，请稍后......')
                    try:
                        time.sleep(10)
                        self.s = socket(AF_INET, SOCK_STREAM)
                        self.s.settimeout(10)
                        self.s.connect(('192.168.1.108', 1008))
                        print('设备连接成功......')
                        break
                    except Exception as e:
                        connect_cnt += 1
                        if connect_cnt > 100:
                            print(f'连接失败，程序退出......')
                            sys.exit(-1)
                    time.sleep(2)
            time.sleep(5)

    def zwdx_send(self, data):
        self.lock.acquire()
        self.s.send(data)
        self.lock.release()

    def zwdx_recv(self):
        msg = self.s.recv(8)
        return msg

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
        self.set_diff_trig_delay(1, 0)
        self.set_diff_trig_delay(2, 0)
        self.set_diff_trig_delay(3, 0)
        self.set_diff_trig_delay(4, 0)
        self.set_diff_trig_delay(5, 0)
        self.set_diff_trig_delay(6, 0)
        self.set_diff_trig_delay(7, 0)
        self.set_diff_trig_delay(8, 0)
        self.set_diff_trig_delay(9, 0)
        self.set_diff_trig_delay(10, 0)
        self.set_diff_trig_delay(11, 0)
        self.set_diff_trig_delay(12, 0)
        self.set_diff_trig_delay(13, 0)
        self.set_diff_trig_delay(14, 0)
        self.set_diff_trig_delay(15, 0)
        self.set_diff_trig_delay(16, 0)
        self.set_diff_trig_delay(17, 0)
        self.set_diff_trig_delay(18, 0)
        self.set_diff_trig_delay(19, 0)
        self.set_diff_trig_delay(20, 0)
        self.set_diff_trig_delay(21, 0)
        self.set_diff_trig_delay(22, 0)
        self.set_diff_trig_delay(23, 0)
        self.set_diff_trig_delay(24, 0)
        self.set_diff_trig_delay(25, 0)
        self.set_diff_trig_delay(26, 0)
        self.set_diff_trig_delay(27, 0)
        self.set_diff_trig_delay(28, 0)
        self.set_diff_trig_delay(29, 0)
        self.set_diff_trig_delay(30, 0)
        self.set_diff_trig_delay(31, 0)
        self.set_diff_trig_delay(32, 0)
        self.set_diff_trig_delay(33, 0)
        self.set_diff_trig_delay(34, 0)
        self.set_diff_trig_delay(35, 0)
        self.set_diff_trig_delay(36, 0)
        self.set_diff_trig_delay(37, 0)
        self.set_diff_trig_delay(38, 0)
        self.set_diff_trig_delay(39, 0)
        self.set_diff_trig_delay(40, 0)
        self.set_diff_trig_delay(41, 0)
        self.set_diff_trig_delay(42, 0)
        self.set_diff_trig_delay(43, 0)
        self.set_diff_trig_delay(44, 0)
        self.set_diff_trig_delay(45, 0)
        self.set_diff_trig_delay(46, 0)
        self.set_diff_trig_delay(47, 0)
        self.set_diff_trig_delay(48, 0)

    def factory_reset(self):
        self.single_sync()
        self.diff_sync()
