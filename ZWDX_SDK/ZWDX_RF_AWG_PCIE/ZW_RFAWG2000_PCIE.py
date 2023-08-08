import numpy as np
import struct
import time
import os
from ctypes import c_int64, c_int16
from socket import socket, AF_INET, SOCK_STREAM
from enum import Enum

base_address = 0x80040000


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
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG11_OFFSET = 44
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG12_OFFSET = 48
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG13_OFFSET = 52
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG14_OFFSET = 56
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG15_OFFSET = 60
    ZWDX_TRIG_CONTROL_S00_AXI_SLV_REG16_OFFSET = 64


class cmd_type(Enum):
    REG_SET_CMD = 0x01
    REG_GET_CMD = 0x02
    SET_CHANNEL_CMD = 0x03
    DWORD_GET_CMD = 0x04
    GET_IQ_RESULT = 0x05
    SET_BOARD_ID = 0x06
    SET_VERIFY_COE = 0x07
    DAC_DATA_START_CMD = 0xDD000000
    DAC_DATA_END_CMD = 0xEE000000


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
    type = None
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


class set_coe(cmd_base):
    hd = 0x55
    id = 0x01
    length = 3
    type = None
    data = []

    def __init__(self):
        super().__init__()

    def create_pack(self):
        self.ad_da_cmd.clear()
        self.ad_da_cmd = [self.hd, self.id, self.length, self.type]
        self.ad_da_cmd += self.data
        return self.build()


class RFAWG2000_PCIE:
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
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.connect((ip, port))
        self.s.settimeout(10)

    def zwdx_send(self, data):
        self.s.send(data)

    def zwdx_recv(self, length):
        msg = self.s.recv(length)
        return msg

    def dev_mem_write(self, base, offset, data):
        cmd = set_reg_cmd()
        cmd.type = cmd_type.REG_SET_CMD.value
        cmd.base_address = base_address
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

    def setbit(self, base, offset, n):
        temp = self.dev_mem_read(base, offset)
        send_temp = (temp | (1 << n))
        self.dev_mem_write(base, offset, send_temp)

    def resetbit(self, base, offset, n):
        temp = self.dev_mem_read(base, offset)
        send_temp = (temp & (~(1 << n)))
        self.dev_mem_write(base, offset, send_temp)

    def setnbit(self, base, offset, nbit):
        temp = self.dev_mem_read(base, offset)
        send_temp = (temp | nbit)
        self.dev_mem_write(base, offset, send_temp)

    def resetnbit(self, base, offset, nbit):
        temp = self.dev_mem_read(base, offset)
        send_temp = (temp & (~nbit))
        self.dev_mem_write(base, offset, send_temp)
    
    def dev_mem_read_dword(self, base, offset):
        cmd = set_reg_cmd()
        cmd.type = cmd_type.DWORD_GET_CMD.value
        cmd.base_address = base
        cmd.offset = offset
        self.zwdx_send(cmd.create_pack())
        msgbytes = self.zwdx_recv(8)
        return int.from_bytes(msgbytes, 'little')

    def set_channel(self, ch):
        cmd = set_reg_cmd()
        cmd.type = cmd_type.SET_CHANNEL_CMD.value
        cmd.base_address = ch  # 借一下基地址做通道号使用
        self.zwdx_send(cmd.create_pack())

    def config_param(self, param: dict):
        """
        配置所需要的参数
        :param ch:
        :param param:参数字典
        :return:
        """
        self.dev_mem_write(base_address, 4*0, param["REG0Ctrl"])   # 配置ADC[1:4]carlibration参数冻结端口使能
        self.dev_mem_write(base_address, 4*1, param["REG1PhaseParamDataLen"])
        self.dev_mem_write(base_address, 4*2, param["REG2AdCollectLen"])
        self.dev_mem_write(base_address, 4 * 3, param["REG3AdCollectDelay"])
        self.dev_mem_write(base_address, 4 * 4, param["REG4Dac1PlayLen"])
        self.dev_mem_write(base_address, 4 * 5, param["REG5Dac2PlayLen"])
        self.dev_mem_write(base_address, 4 * 6, param["REG6Dac3PlayLen"])
        self.dev_mem_write(base_address, 4 * 7, param["REG7Dac4PlayLen"])
        self.dev_mem_write(base_address, 4 * 8, param["REG8Dac5PlayLen"])

        self.dev_mem_write(base_address, 4 * 11, param["REG11Dac5PlayDelay"])
        self.dev_mem_write(base_address, 4 * 9, param["REG9Dac12PlayDelay"])
        self.dev_mem_write(base_address, 4 * 10, param["REG10Dac34PlayDelay"])
        self.dev_mem_write(base_address, 4 * 11, 0x0001FFFF)
        self.dev_mem_write(base_address, 4 * 9, 0xFFFFFFFF)
        self.dev_mem_write(base_address, 4 * 10, 0xFFFFFFFF)

        self.dev_mem_write(base_address, 4 * 12, param["REG12RefClkPhaseL32bit"])
        self.dev_mem_write(base_address, 4 * 13, param["REG13RefClkPhaseH16bit"])
        self.dev_mem_write(base_address, 4 * 14, param["REG14RefClkFsL32bit"])
        self.dev_mem_write(base_address, 4 * 15, param["REG15RefClkFsH16bit"])

        self.dev_mem_write(base_address, 4 * 12, 0x00000000)
        self.dev_mem_write(base_address, 4 * 13, 0x00020000)
        self.dev_mem_write(base_address, 4 * 14, 0x00000000)
        self.dev_mem_write(base_address, 4 * 15, 0x00002000)

        self.dev_mem_write(base_address, 4 * 12, 0x00000000)
        self.dev_mem_write(base_address, 4 * 13, 0x00030000)
        self.dev_mem_write(base_address, 4 * 14, 0x00000000)
        self.dev_mem_write(base_address, 4 * 15, 0x00001000)

        self.dev_mem_write(base_address, 4 * 12, 0x00000000)
        self.dev_mem_write(base_address, 4 * 13, 0x00040000)
        self.dev_mem_write(base_address, 4 * 14, 0x00000000)
        self.dev_mem_write(base_address, 4 * 15, 0x00004000)

    def send_dac_file(self, ch, ap: str):
        """
        发送DAC文件数据到DAC
        :param ch:
        :param ap: absolute path 文件绝对路径
        :return:
        """
        self.set_channel(ch)
        fd = open(ap, "rb")
        fsize = os.path.getsize(ap)
        integer = fsize // 512
        remainder = fsize % 512
        target = cmd_base()
        target.head = 0xF3F2F1F0
        target.cmd = cmd_type.DAC_DATA_START_CMD.value
        target.len = int.from_bytes(np.asarray(512, np.uint32).byteswap(), "little")
        for i in range(integer):
            target.ad_da_cmd.clear()
            target.ad_da_cmd = np.frombuffer(fd.read(512), np.uint8).tolist()
            self.zwdx_send(target.build())
        target.cmd = cmd_type.DAC_DATA_END_CMD.value
        target.len = int.from_bytes(np.asarray(remainder, np.uint32).byteswap(), "little")
        target.ad_da_cmd.clear()
        target.ad_da_cmd = np.frombuffer(fd.read(remainder), np.uint8).tolist()
        self.zwdx_send(target.build())
        target.head = 0xF7F6F5F4

    def send_dac_data(self, ch, data):
        """
        发送直接数据到DAC，注意字节序问题
        :param ch: 通道
        :param data: 数据
        :return:
        """
        self.set_channel(ch)
        cshort = np.asarray(data, dtype=np.int16)
        datalist = list(cshort.tobytes())
        integer = len(datalist) // 512
        remainder = len(datalist) % 512
        target = cmd_base()
        target.head = 0xF3F2F1F0
        target.cmd = cmd_type.DAC_DATA_START_CMD.value
        target.len = int.from_bytes(np.asarray(512, np.uint32).byteswap(), "little")
        for i in range(integer):
            target.ad_da_cmd.clear()
            target.ad_da_cmd = datalist[i*512:i*512 + 512]
            self.zwdx_send(target.build())
            # time.sleep(0.01)
        target.cmd = cmd_type.DAC_DATA_END_CMD.value
        target.len = int.from_bytes(np.asarray(remainder, np.uint32).byteswap(), "little")
        target.ad_da_cmd.clear()
        target.ad_da_cmd = datalist[integer*512:integer*512 + remainder]
        self.zwdx_send(target.build())
        target.head = 0xF7F6F5F4

    def dac_play_user(self, pt: int):
        """
        播放采集
        :param pt: 播放次数
        :return:
        """
        IQ = []
#         self.setbit(base_address, 0, 4)
        for i in range(pt):
            self.dac_play()
        while True:
            time.sleep(1)
            ready = self.dev_mem_read(base_address, 4*21)
            if ready == 1:
                break
        # for i in range(pt):
        #     IQ.append(self.get_iq_result(1, i*64))
        # return IQ
        # result = self.get_iq_result_new(pt)
        # return result

    def dac_play(self):
        """
        启动DAC播放
        :return:
        """
        self.dev_mem_write(base_address, 0, 0x80007C30)  # soft trig en
        #self.resetbit(base_address, 0, 3)
        time.sleep(1e-6)
        self.dev_mem_write(base_address, 0, 0x80007C38)  # soft tig
        #self.setbit(base_address, 0, 3)
        time.sleep(0.001)

    def get_iq_result(self, ch, offset):
        # # self.dev_mem_write(base_address, 0, 0xF0000029)
        # # self.dev_mem_write(base_address, 0, 0xF000002D)
        # # time.sleep(0.01)
        # ih = self.dev_mem_read(base_address, 4 * 16)
        # il = self.dev_mem_read(base_address, 4 * 17)
        # qh = self.dev_mem_read(base_address, 4 * 18)
        # ql = self.dev_mem_read(base_address, 4 * 19)
        #
        # I = c_int64(c_int16(ih).value * (0xFFFFFFFF + 1)).value + c_int64(il).value
        # Q = c_int64(c_int16(qh).value * (0xFFFFFFFF + 1)).value + c_int64(ql).value
        # # I = (ih << 32) | il
        # # Q = (qh << 32) | ql

        if ch == 1:
            I = self.dev_mem_read_dword(0x86000000 + 48, offset)
            Q = self.dev_mem_read_dword(0x86000000 + 56, offset)
            # python 没有类型，多大都能装，所以要进行数据类型转换
            # print(f'I:{c_int64(I).value}, Q:{c_int64(Q).value}')
        return c_int64(I).value, c_int64(Q).value

    def get_iq_result_new(self, length):
        cmd = set_reg_cmd()
        cmd.type = cmd_type.GET_IQ_RESULT.value
        # self.zwdx_send(cmd.create_pack())
        msgbytes = b''
        read_cnt = length * 16
        # while read_cnt:
        #     tempdata = self.zwdx_recv(read_cnt)
        #     msgbytes += tempdata
        #     read_cnt -= len(tempdata)
        interge = read_cnt // 512
        remainder = read_cnt % 512
        if remainder != 0:
            interge += 1
        # 垃圾LWIP,一对一请求传输数据
        for i in range(interge):
            cmd.base_address = i
            self.zwdx_send(cmd.create_pack())
            msgbytes += self.zwdx_recv(512)
            time.sleep(0.01)
        tempbytes = msgbytes[:read_cnt]
        buffer = np.frombuffer(tempbytes, np.int64)
        # print(buffer)
        return buffer

    def set_pcie_board_id(self, id):
        cmd = set_reg_cmd()
        cmd.type = cmd_type.SET_BOARD_ID.value
        cmd.base_address = id  # 借一下基地址做ID使用
        self.zwdx_send(cmd.create_pack())

    def set_coeff_verify(self, param: dict):
        cmd = set_coe()
        cmd.type = cmd_type.SET_VERIFY_COE.value
        tempdata = []
        for i in param:
            tempdata.append(param[i])
        nparr = np.asarray(tempdata, np.uint32)
        cmd.data = nparr.view("uint8").tolist()
        self.zwdx_send(cmd.create_pack())




