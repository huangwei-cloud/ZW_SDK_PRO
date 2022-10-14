import ZW_DC1000

if __name__ == '__main__':

    # 获取设备对象
    obj = ZW_DC1000.DC1000()

    # 连接根据硬件连接方式二选一
    # 以太网方式连接设备
    obj.ethernet_connect("192.168.1.20", 8080)

    # 串口方式连接设备
    obj.uart_connect("COM3")

    # 设置斜率
    obj.set_slope(1000)

    # 打开通道
    obj.open_ch(1)

    # 关闭通道
    obj.close_ch(1)

    # 设置电压
    obj.set_vol(1, 5)

    # 获取电流
    obj.get_current(1)

    # 使能通道端接电阻
    obj.R_TERM(1, 1)

    # 使能通道端接电容
    obj.C_TERM(1, 1)

    # 使能通道电流采集功能
    obj.IVDIS(1, 1)

    # 检测设备在线状态，可以作为心跳使用
    obj.check_device_status()

    # 改变设备IP, 不用重启设备，改变后自动生效
    obj.change_ip("192.168.1.100")




