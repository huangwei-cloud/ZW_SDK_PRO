import struct
import serial
import numpy as np
import socket
import time


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
    gw = []
    crc = 0
    end = 0xaa

    def __init__(self, ip=[], mask=[], gw=[]):
        super().__init__()
        self.ip = ip
        self.mask = mask
        self.gw = gw

    def create_pack(self):
        buffer = [self.hd, self.id, self.length, self.type]
        buffer += self.ip
        buffer += self.mask
        buffer += self.gw
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
    ch = 0
    crc = 0
    end = 0xaa

    def __init__(self):
        super().__init__()
        pass

    def create_pack(self):
        buffer = [self.hd, self.id, self.length, self.type, self.ch, self.crc, self.end]
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


class get_ip_cmd(cmd_base):
    hd = 0x55
    id = 0x01
    length = 8
    type = 0x12
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
        self.k = 0

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

        assert 1 <= port <= 65535, 'input param error,please check[1,65535]'
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

    def _check_device_status(self):
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

    def set_ip_mask(self, ip='', mask='255.255.255.0', gw='192.168.1.1'):
        """
        :param ip:
        :param mask:
        :param gw:
        :return:
        """
        ip_list = ip.split('.')
        int_ip_list = list(map(int, ip_list))
        mask_list = mask.split('.')
        int_mask_list = list(map(int, mask_list))
        gw_list = gw.split('.')
        int_gw_list = list(map(int, gw_list))
        cmd = ip_cmd(int_ip_list, int_mask_list, int_gw_list)
        self.zwdx_send(cmd.create_pack())

    def get_ip_mask(self):
        """
        获取设备IP和子网掩码MASK
        :return:
        """
        cmd = get_ip_cmd()
        self.zwdx_send(cmd.create_pack())
        msg = self.zwdx_recv(12)
        ip, mask, gw = struct.unpack('!III', msg)
        ip_str = socket.inet_ntoa(struct.pack('I', socket.htonl(ip)))
        mask_str = socket.inet_ntoa(struct.pack('I', socket.htonl(mask)))
        gw_str = socket.inet_ntoa(struct.pack('I', socket.htonl(gw)))
        return {'ip': ip_str, 'mask': mask_str, 'gw': gw_str}

    def set_vol(self, ch: list, vol):
        """
        设置DA输出电压
        :param ch: [1, 5, 8]
        :param vol: 电压值[-10, 10]V
        """
        assert -10 <= vol <= 10, "input param error,please check[-10, 10]."
        cmd = vol_cmd()
        status = None
        for i in ch:
            if i == 0:
                for chnum in range(1, 9, 1):
                    cmd.ch = chnum + 8
                    b = format(vol, '.6f').encode('utf-8')
                    length = len(b)
                    cmd.vol.clear()
                    for cnt in range(8):
                        if cnt < length:
                            cmd.vol.append(b[cnt])
                        else:
                            cmd.vol.append(0)
                    self.zwdx_send(cmd.create_pack())
                    status = self.get_status()
            else:
                cmd.ch = i + 8
                b = format(vol, '.6f').encode('utf-8')
                length = len(b)
                cmd.vol.clear()
                for cnt in range(8):
                    if cnt < length:
                        cmd.vol.append(b[cnt])
                    else:
                        cmd.vol.append(0)
                self.zwdx_send(cmd.create_pack())
                status = self.get_status()
        if status == 0x11:
            print('channel not open')
        return status

    def _get_vol_dac(self, ch: list):
        """
        获取电压值,私有
        :param ch:COM_CH1-COM_CH8
        :return: 返回电压值 单位A
        """
        # assert COM_CH.CH1.value <= ch.value <= COM_CH.CH8.value, "input param error,please check."
        cmd = get_vol_dac_cmd()
        rtn_list = []
        for i in ch:
            if i == 0:
                for chnum in range(1, 9, 1):
                    cmd.ch = chnum + 8
                    self.zwdx_send(cmd.create_pack())
                    msg = self.zwdx_recv(15)
                    a, b, c, d, e, vol, k, f, g = struct.unpack('!BBBBBIIBB', msg)
                    self.k = k
                    rtn_vol = round(vol * 20 / 0xFFFFF - 10, 6)
                    rtn_list.append(rtn_vol)
            else:
                cmd.ch = i + 8
                self.zwdx_send(cmd.create_pack())
                msg = self.zwdx_recv(15)
                a, b, c, d, e, vol, k, f, g = struct.unpack('!BBBBBIIBB', msg)
                self.k = k
                rtn_vol = round(vol * 20 / 0xFFFFF - 10, 6)
                rtn_list.append(rtn_vol)
        return rtn_list

    def get_vol(self, ch: list):
        """
        获取电压值,开放给用户
        :param ch:[1, 2]
        :return: 返回电压值 单位V
        """
        # assert COM_CH.CH1.value <= ch.value <= COM_CH.CH8.value, "input param error,please check."
        cmd = get_vol_cmd()
        rtn_list = []
        for i in ch:
            if i == 0:
                for chnum in range(1, 9, 1):
                    cmd.ch = chnum + 8
                    self.zwdx_send(cmd.create_pack())
                    msg = self.zwdx_recv(15)
                    a, b, c, d, e, vol, k, f, g = struct.unpack('!BBBBBIIBB', msg)
                    self.k = k
                    rtn_vol = round(vol * 20 / 0xFFFFF - 10, 6)
                    rtn_list.append(rtn_vol)
            else:
                cmd.ch = i + 8
                self.zwdx_send(cmd.create_pack())
                msg = self.zwdx_recv(15)
                a, b, c, d, e, vol, k, f, g = struct.unpack('!BBBBBIIBB', msg)
                self.k = k
                rtn_vol = round(vol * 20 / 0xFFFFF - 10, 6)
                rtn_list.append(rtn_vol)

        return rtn_list

    def set_volt_slope(self, slope):
        """
        设置上升或下降的斜率
        :param slope:单位mv/s.默认1000mv/s，范围[1-1000000]
        """
        assert 1 <= slope <= 1000000, 'input param error[1-1000000]'
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
        if ch == 0:
            for i in range(1, 9, 1):
                cmd.ch = i + 8
                self.zwdx_send(cmd.create_pack())
                status = self.get_status()
        else:
            cmd.ch = ch + 8
            self.zwdx_send(cmd.create_pack())
            status = self.get_status()
        return status

    def _close_ch(self, ch, mode):
        cmd = open_close_cmd()
        cmd.switch = mode
        status = None
        if ch == 0:
            for i in range(1, 9, 1):
                cmd.ch = i + 8
                self.zwdx_send(cmd.create_pack())
                status = self.get_status()
        else:
            cmd.ch = ch + 8
            self.zwdx_send(cmd.create_pack())
            status = self.get_status()
        return status

    def set_ch_on(self, ch: list):
        """
        安全打开多通道
        :param ch:通道列表 例如:[1, 2]
        :return:返回执行结果 0xFF:表示成功
        """
        status = None
        for i in ch:
            status = self._open_ch(i, 1)
        return status

    def set_ch_off(self, ch: list):
        """
        安全关闭多通道
        :param ch:通道列表 例如:[1, 2, 3, 4]
        :return:返回执行结果 0xFF:表示成功
        """
        status = None

        temp = self.get_vol(ch)
        vol_list = list(map(abs, temp))
        self.set_vol(ch, 0)
        delay = max(vol_list) / (self.k / 1000)
        time.sleep(delay)
        for i in ch:
            status = self._close_ch(i, 2)
        return status

    def _set_ch_off_fast(self, ch: list):
        """
        快速关闭多通道
        :param ch:通道列表 例如:[1, 2]
        :return: 返回执行结果 0xFF:表示成功
        """
        status = None
        temp = self.get_vol(ch)
        vol_list = list(map(abs, temp))
        self.set_res_option(ch, 1)
        for i in ch:
            self._close_ch(i, 2)
        self.set_vol(ch, 0)
        delay = max(vol_list) / (self.k / 1000)
        time.sleep(delay)
        status = self.set_res_option(ch, 0)
        return status

    def get_ch_status(self, ch: list):
        """
        获取单个通道的开关状态
        :param ch: [1, 5, 8]
        :return: 1:open 0: off
        """
        st_list = []
        cmd = status_cmd()
        for i in ch:
            if i == 0:
                for chnum in range(1, 9, 1):
                    cmd.ch = chnum
                    self.zwdx_send(cmd.create_pack())
                    recvmsg = self.zwdx_recv(7)
                    temptup = struct.unpack('BBBBBBB', recvmsg)
                    st_list.append(temptup[4])
            else:
                cmd.ch = i
                self.zwdx_send(cmd.create_pack())
                recvmsg = self.zwdx_recv(7)
                temptup = struct.unpack('BBBBBBB', recvmsg)
                st_list.append(temptup[4])

        return st_list

    def get_current(self, ch: list):
        """
        获取通道电流
        :param ch: [1,2,3,4]
        :return: 单位A
        """
        # assert COM_CH.CH1.value <= ch.value <= COM_CH.CH8.value, "input param error,please check."
        cmd = current_cmd()
        current_list = []
        for i in ch:
            if i == 0:
                for chnum in range(1, 9, 1):
                    cmd.ch = chnum
                    self.zwdx_send(cmd.create_pack())
                    msg = self.zwdx_recv(15)
                    a, b, c, d, e, current, k, f, g = struct.unpack('!BBBBBiIBB', msg)
                    current_list.append(current / 1000 / 1000 / 1000 / 1000)
            else:
                cmd.ch = i
                self.zwdx_send(cmd.create_pack())
                msg = self.zwdx_recv(15)
                a, b, c, d, e, current, k, f, g = struct.unpack('!BBBBBiIBB', msg)
                current_list.append(current / 1000 / 1000 / 1000 / 1000)
        return current_list

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

    def set_dis(self, ch, type, st):
        cmd = set_ch_dis()
        cmd.ch = ch
        cmd.ty = type
        cmd.st = st
        self.zwdx_send(cmd.create_pack())
        return self.get_status()

    def set_res_option(self, ch: list, val: int):
        """
        设置某个通道端接电阻1MΩ使能
        :param ch:[1, 5, 8]
        :param val: 使能：1 不使能：0
        :return:状态信号
        """
        # assert COM_CH.CH1.value <= ch.value <= COM_CH.CH8.value, "input param error,please check."
        status = None
        for i in ch:
            if i == 0:
                for chnum in range(1, 9, 1):
                    status = self.set_dis(chnum - 1, 0, val)
            else:
                status = self.set_dis(i - 1, 0, val)
        return status

    def set_cap_option(self, ch: list, val: int):
        """
        设置某个通道端接电容1uF使能
        :param ch:[1, 5, 8]
        :param val: 使能：1 不使能：0
        :return:状态信号
        """
        # assert COM_CH.CH1.value <= ch.value <= COM_CH.CH8.value, "input param error,please check."
        status = None
        for i in ch:
            if i == 0:
                for chnum in range(1, 9, 1):
                    status = self.set_dis(chnum - 1, 1, val)
            else:
                status = self.set_dis(i - 1, 1, val)
        return status

    def set_iv_option(self, ch: list, val: int):
        """
        设置某个通道电流采集功能
        :param ch:[1, 5, 8]
        :param val: 使能：1 不使能：0
        :return:状态信号
        """
        # assert COM_CH.CH1.value <= ch.value <= COM_CH.CH8.value, "input param error,please check."
        status = None
        for i in ch:
            if i == 0:
                for chnum in range(1, 9, 1):
                    status = self.set_dis(chnum - 1, 2, val)
            else:
                status = self.set_dis(i - 1, 2, val)
        return status

    def _set_pwm_status(self, ch: list, val: int):
        """
        使能PWM调节2uv精度，内部测试使用
        :param ch:[1, 5, 8]
        :param val:使能：1 不使能：0
        :return: 状态信号0xFF
        """
        # assert COM_CH.CH1.value <= ch.value <= COM_CH.CH8.value, "input param error,please check."
        status = None
        for i in ch:
            if i == 0:
                for chnum in range(1, 9, 1):
                    status = self.set_dis(chnum - 1, 3, val)
            else:
                status = self.set_dis(i - 1, 3, val)
        return status

    def _set_reset_volt_slop(self, slop):
        """
        设置设备后面复位按钮下降斜率，内部测试使用
        :param slop:斜率mv/s
        :return: 执行结果 0xFF:成功
        """
        assert 1 <= slop <= 1000000, 'input slope error[1-1000000]'
        cmd = reset_slope_cmd()
        cmd.slope = slop
        self.zwdx_send(cmd.create_pack())
        return self.get_status()
