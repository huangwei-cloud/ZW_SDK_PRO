import ZW_DC1000

if __name__ == '__main__':
    # 获取设备对象
    obj = ZW_DC1000.DC1000()

    # 连接根据硬件连接方式二选一
    # 以太网方式连接设备
    obj.ethernet_connect("127.0.0.1", 8080)

    # 串口方式连接设备
    obj.uart_connect("COM3")

    # 设置电压上升/下降斜率
    obj.set_volt_slope(1000)

    # 打开/关闭通道
    obj.set_ch_status(ZW_DC1000.ZW_CH.CH1, ZW_DC1000.ZW_STATUS.OPEN)  # 安全打开通道1
    obj.set_ch_status(ZW_DC1000.ZW_CH.CH1, ZW_DC1000.ZW_STATUS.CLOSE)  # 安全关闭通道1
    obj.set_ch_status(ZW_DC1000.ZW_CH.CHALL, ZW_DC1000.ZW_STATUS.OPEN)  # 安全打开所有通道
    obj.set_ch_status(ZW_DC1000.ZW_CH.CHALL, ZW_DC1000.ZW_STATUS.CLOSE)  # 安全关闭所有通道

    obj.set_ch_status_fast(ZW_DC1000.ZW_CH.CH1, ZW_DC1000.ZW_STATUS.OPEN)  # 安全打开通道1
    obj.set_ch_status_fast(ZW_DC1000.ZW_CH.CH1, ZW_DC1000.ZW_STATUS.CLOSE)  # 快速关闭通道1
    obj.set_ch_status_fast(ZW_DC1000.ZW_CH.CHALL, ZW_DC1000.ZW_STATUS.OPEN)  # 安全打开所有通道
    obj.set_ch_status_fast(ZW_DC1000.ZW_CH.CHALL, ZW_DC1000.ZW_STATUS.CLOSE)  # 快速关闭所有通道

    # 设置电压
    obj.set_vol(ZW_DC1000.ZW_CH.CH1, 5)  # 通道1设置5V电压
    obj.set_vol(ZW_DC1000.ZW_CH.CH2, -5)  # 通道2设置-5V电压

    # 获取电压
    ch1vol = obj.get_vol(ZW_DC1000.ZW_CH.CH1)  # 获取通道1电压
    ch2vol = obj.get_vol(ZW_DC1000.ZW_CH.CH2)  # 获取通道2电压

    # 从DAC获取电压
    ch1voldac = obj.get_vol(ZW_DC1000.ZW_CH.CH1)  # 获取通道1电压
    ch2voldac = obj.get_vol(ZW_DC1000.ZW_CH.CH2)  # 获取通道2电压

    # 获取电流
    ch1a = obj.get_current(ZW_DC1000.ZW_CH.CH1)  # 获取通道1电流
    ch2a = obj.get_current(ZW_DC1000.ZW_CH.CH2)  # 获取通道2电流

    # 使能通道端接电阻
    obj.res_term(ZW_DC1000.ZW_CH.CH1, ZW_DC1000.ZW_STATUS.ENABLE)  # 使能通道1端接电阻
    obj.res_term(ZW_DC1000.ZW_CH.CH1, ZW_DC1000.ZW_STATUS.DISABLE)  # 禁用通道1端接电阻

    # 使能通道端接电容
    obj.cap_term(ZW_DC1000.ZW_CH.CH1, ZW_DC1000.ZW_STATUS.ENABLE)  # 使能通道1端接电容
    obj.cap_term(ZW_DC1000.ZW_CH.CH1, ZW_DC1000.ZW_STATUS.DISABLE)  # 禁用通道1端接电容

    # 通道电流采集功能
    obj.iv_term(ZW_DC1000.ZW_CH.CH1, ZW_DC1000.ZW_STATUS.ENABLE)  # 启用通道1电流采集功能
    obj.iv_term(ZW_DC1000.ZW_CH.CH1, ZW_DC1000.ZW_STATUS.DISABLE)  # 禁用通道1电流采集功能

    # 使能PWM调节精度到2uv
    obj._set_pwm_status(ZW_DC1000.ZW_CH.CH1, ZW_DC1000.ZW_STATUS.ENABLE)  # 使能通道1PWM

    # 设置设备后面复位按钮复位斜率
    obj._set_reset_slop(1000)   # 设置复位斜率1000mv/s

    # 检测设备在线状态，可以作为心跳使用
    obj.check_device_status()

    # 改变设备IP, 不用重启设备，改变后自动生效
    obj.change_ip("192.168.1.100")
