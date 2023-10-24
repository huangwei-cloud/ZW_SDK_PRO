import numpy as np
import struct
import time
import serial
import socket
import sys
from enum import Enum

base_address = 0x43C0_0000
clk_base_address = 0x83C0_0000


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
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG61_OFFSET = 244
    # 模式设置
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG62_OFFSET = 248
    # 通道1-10脉冲频率
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG63_OFFSET = 252
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG64_OFFSET = 256
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG65_OFFSET = 260
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG66_OFFSET = 264
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG67_OFFSET = 268
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG68_OFFSET = 272
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG69_OFFSET = 276
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG70_OFFSET = 280
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG71_OFFSET = 284
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG72_OFFSET = 288
    # 通道1-10脉冲个数
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG73_OFFSET = 292
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG74_OFFSET = 296
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG75_OFFSET = 300
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG76_OFFSET = 304
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG77_OFFSET = 308
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG78_OFFSET = 312
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG79_OFFSET = 316
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG80_OFFSET = 320
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG81_OFFSET = 324
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG82_OFFSET = 328
    # 同步命令
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG83_OFFSET = 332


class cmd_type(Enum):
    REG_SET_CMD = 0x01
    REG_GET_CMD = 0x02
    REG_SET_CMD_SHORT = 0x03


class TMU_CLKSRC_OPTION(Enum):
    INTERNAL_100MHZ = 0
    EXTERNAL_100MHZ = 1
    EXTERNAL_10MHZ = 2


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


class TMU1000:
    connect_mode = None
    ch_status = 0

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
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, True)
        if sys.platform == "win32":
            self.s.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 60 * 1000, 10 * 1000))
        else:
            self.s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60)
            self.s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 3)
            self.s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)
        self.s.connect((ip, port))
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

    def dev_mem_write(self, base, offset, data):
        cmd = set_reg_cmd()
        cmd.type = cmd_type.REG_SET_CMD.value
        cmd.base_address = base
        cmd.offset = offset
        cmd.reg = data
        self.zwdx_send(cmd.create_pack())

    def dev_mem_read(self, base, offset):
        cmd = set_reg_cmd()
        cmd.type = cmd_type.REG_GET_CMD.value
        cmd.base_address = base
        cmd.offset = offset
        self.zwdx_send(cmd.create_pack())
        msgbytes = self.zwdx_recv(4)
        return int.from_bytes(msgbytes, 'little')

    def dev_mem_write_short(self, base, offset, data):
        cmd = set_reg_cmd()
        cmd.type = cmd_type.REG_SET_CMD_SHORT.value
        cmd.base_address = base
        cmd.offset = offset
        cmd.reg = data
        self.zwdx_send(cmd.create_pack())

    def set_trig_time(self, T):
        # assert fs_hz % 5 == 0, "error input, input is an integer multiple of 5"
        self.dev_mem_write(base_address, axi_slv_reg_offset.ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG0_OFFSET.value, T)

    def set_diff_trig_time(self, T):
        # assert fs_hz % 5 == 0, "error input, input is an integer multiple of 5"
        self.dev_mem_write(base_address, axi_slv_reg_offset.ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG60_OFFSET.value, T)

    def set_trig_delay(self, ch, value_ps):
        # assert 1 <= ch <= 10, "please check channel value[1-10]"
        for i in axi_slv_reg_offset:
            if i.value == ch * 4:
                self.dev_mem_write(base_address, i.value, value_ps)

    def set_diff_trig_delay(self, ch, value_ps):
        assert 1 <= ch <= 10, "input param error[1,10]"
        for i in axi_slv_reg_offset:
            if i.value == (ch + 11) * 4:
                self.dev_mem_write(base_address, i.value, value_ps)

    def close_channel(self, ch: int):
        assert 1 <= ch <= 10, "input param error[1,10]"
        self.ch_status &= ~(1 << (ch - 1))
        self.dev_mem_write(base_address, axi_slv_reg_offset.ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG11_OFFSET.value, self.ch_status)

    def open_channel(self, ch: int):
        assert 1 <= ch <= 10, "input param error[1,10]"
        self.ch_status |= (1 << (ch - 1))
        self.dev_mem_write(base_address, axi_slv_reg_offset.ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG11_OFFSET.value, self.ch_status)

    def init(self, ref):
        """
        设置内外参考，以及时钟频率选择
        :param ref: 内外参考时钟，枚举表示,内时钟默认100MHz,外时钟10/100MHz
        :return:
        """
        clk = 0
        if ref == TMU_CLKSRC_OPTION.INTERNAL_100MHZ:
            clk = 100
            self.dev_mem_write(base_address, axi_slv_reg_offset.ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG61_OFFSET.value, 0)
        elif ref == TMU_CLKSRC_OPTION.EXTERNAL_10MHZ:
            clk = 10
            self.dev_mem_write(base_address, axi_slv_reg_offset.ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG61_OFFSET.value, 2)
        elif ref == TMU_CLKSRC_OPTION.EXTERNAL_100MHZ:
            clk = 100
            self.dev_mem_write(base_address, axi_slv_reg_offset.ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG61_OFFSET.value, 2)
        else:
            print(f"input param error...")
        
        self.dev_mem_write(clk_base_address, 0x00, 0x0000000A)
        self.dev_mem_write(clk_base_address, 0x0C, 0x00000000)
        self.dev_mem_write(clk_base_address, 0x10, 0x00000000)

        if clk == 100:
            self.dev_mem_write_short(clk_base_address, 0x300, 0xFFFF)
            self.dev_mem_write_short(clk_base_address, 0x304, 0x1cb2)
            self.dev_mem_write_short(clk_base_address, 0x308, 0x0000)
            self.dev_mem_write_short(clk_base_address, 0x30C, 0x1145)
            self.dev_mem_write_short(clk_base_address, 0x310, 0x0000)
            self.dev_mem_write_short(clk_base_address, 0x314, 0x1083)
            self.dev_mem_write_short(clk_base_address, 0x318, 0x0080)
            self.dev_mem_write_short(clk_base_address, 0x31C, 0x1041)
            self.dev_mem_write_short(clk_base_address, 0x320, 0x00C0)
            self.dev_mem_write_short(clk_base_address, 0x324, 0x1041)
            self.dev_mem_write_short(clk_base_address, 0x328, 0x00C0)
            self.dev_mem_write_short(clk_base_address, 0x32C, 0x1041)
            self.dev_mem_write_short(clk_base_address, 0x330, 0x00C0)
            self.dev_mem_write_short(clk_base_address, 0x334, 0x1041)
            self.dev_mem_write_short(clk_base_address, 0x338, 0x00C0)
            self.dev_mem_write_short(clk_base_address, 0x33C, 0x1041)
            self.dev_mem_write_short(clk_base_address, 0x340, 0x1145)
            self.dev_mem_write_short(clk_base_address, 0x344, 0x0000)
            self.dev_mem_write_short(clk_base_address, 0x348, 0x01e8)
            self.dev_mem_write_short(clk_base_address, 0x34C, 0x7001)
            self.dev_mem_write_short(clk_base_address, 0x350, 0x71E9)
            self.dev_mem_write_short(clk_base_address, 0x354, 0x0800)
            self.dev_mem_write_short(clk_base_address, 0x358, 0x1100)
        elif clk == 10:
            self.dev_mem_write_short(clk_base_address, 0x300, 0xFFFF)
            self.dev_mem_write_short(clk_base_address, 0x304, 0x179e)
            self.dev_mem_write_short(clk_base_address, 0x308, 0x0000)
            self.dev_mem_write_short(clk_base_address, 0x30C, 0x10c3)
            self.dev_mem_write_short(clk_base_address, 0x310, 0x0000)
            self.dev_mem_write_short(clk_base_address, 0x314, 0x1042)
            self.dev_mem_write_short(clk_base_address, 0x318, 0x0080)
            self.dev_mem_write_short(clk_base_address, 0x31C, 0x1041)
            self.dev_mem_write_short(clk_base_address, 0x320, 0x00C0)
            self.dev_mem_write_short(clk_base_address, 0x324, 0x1041)
            self.dev_mem_write_short(clk_base_address, 0x328, 0x00C0)
            self.dev_mem_write_short(clk_base_address, 0x32C, 0x1041)
            self.dev_mem_write_short(clk_base_address, 0x330, 0x00C0)
            self.dev_mem_write_short(clk_base_address, 0x334, 0x1041)
            self.dev_mem_write_short(clk_base_address, 0x338, 0x00C0)
            self.dev_mem_write_short(clk_base_address, 0x33C, 0x1041)
            self.dev_mem_write_short(clk_base_address, 0x340, 0x179e)
            self.dev_mem_write_short(clk_base_address, 0x344, 0x0000)
            self.dev_mem_write_short(clk_base_address, 0x348, 0x00fa)
            self.dev_mem_write_short(clk_base_address, 0x34C, 0x7c01)
            self.dev_mem_write_short(clk_base_address, 0x350, 0x7dE9)
            self.dev_mem_write_short(clk_base_address, 0x354, 0x0800)
            self.dev_mem_write_short(clk_base_address, 0x358, 0x0800)
        else:
            print("input clk error...")
        time.sleep(1)
        status = self.dev_mem_read(clk_base_address, 0x04)
        if status == 0x01:
            self.dev_mem_write(clk_base_address, 0x35C, 0x03)
        else:
            print("clk not lock...")
            
        time.sleep(1)
        status = self.dev_mem_read(clk_base_address, 0x35C) & 0x01
        if status != 0:
            print("sync clk not lock...")
        # self.single_init() config verify param
        self.set_trig_delay(1, 166)
        time.sleep(0.5)
        self.set_trig_delay(2, 169)
        time.sleep(0.5)
        self.set_trig_delay(3, 141)
        time.sleep(0.5)
        self.set_trig_delay(4, 0)
        time.sleep(0.5)
        self.set_trig_delay(5, 100)
        time.sleep(0.5)
        self.set_trig_delay(6, 189)
        time.sleep(0.5)
        self.set_trig_delay(7, 18)
        time.sleep(0.5)
        self.set_trig_delay(8, 13)
        time.sleep(0.5)
        self.set_trig_delay(9, 153)
        time.sleep(0.5)
        self.set_trig_delay(10, 48)

    def set_work_mode(self, mode: int):
        """
        设置模式
        :param mode:0：扇出trigger fanout 1: 自己产生self-generate
        :return:
        """
        assert 0 <= mode <= 1, "input param error..."
        self.dev_mem_write(base_address, axi_slv_reg_offset.ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG62_OFFSET.value, mode)

    def set_pulse_period(self, ch: int, time_ns: int):
        """
        设置脉冲频率
        :param time_ns:
        :param ch:通道1-10
        :param time_ns:(ns) 最小10ns, 步进10ns
        :return:
        """
        freq = time_ns//10
        assert 1 <= ch <= 10, "input param error[1-10]"
        for i in axi_slv_reg_offset:
            if i.value == (ch + 62) * 4:
                self.dev_mem_write(base_address, i.value, freq)

    def set_pulse_number(self, ch: int, number: int):
        """
        设置脉冲个数
        :param ch:通道1-10
        :param number:0:表示连续输出  n:表示脉冲个数
        :return:
        """
        assert 1 <= ch <= 10, "input param error[1-10]"
        for i in axi_slv_reg_offset:
            if i.value == (ch + 72) * 4:
                self.dev_mem_write(base_address, i.value, number)

    def one_shot_sync(self, mode: int):
        """
        同步一次，选择同步源
        :param mode:0：软触发，通道自身同步 1：硬触发，外部trigger
        :return:
        """
        assert 0 <= mode <= 1, "input param error..."
        self.dev_mem_write(base_address, axi_slv_reg_offset.ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG83_OFFSET.value, mode)
        time.sleep(0.01)
        self.dev_mem_write(base_address, axi_slv_reg_offset.ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG83_OFFSET.value, (1 << 16) | mode)

    def diff_sync(self):
        for i in range(1, 49, 1):
            self.set_diff_trig_delay(i, 0)

