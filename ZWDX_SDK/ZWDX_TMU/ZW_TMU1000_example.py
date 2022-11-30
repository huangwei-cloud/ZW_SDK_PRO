import ZW_TMU1000

if __name__ == "__main__":
    obj = ZW_TMU1000.TMU1000()

    # 连接根据硬件连接方式二选一
    # 以太网方式连接设备
    obj.ethernet_connect("192.168.1.20", 8080)

    # 串口方式连接设备
    obj.uart_connect("COM3")

    #
    obj.single_sync()

    # 打开通道
    obj.open_channel(1)

    # 关闭通道
    obj.close_channel(1)

    # 单端频率，延时值设置
    obj.set_trig_time(100)

    # 差分频率延时值设置
    obj.set_diff_trig_time(100)

    # 单端触发延时
    obj.set_trig_delay(1, 100)

    # 差分触发延时
    obj.set_diff_trig_delay(1, 100)

    # 设置外参考
    obj.set_refclk("ext_ref")

    # 复位
    obj.factory_reset()

    # 检测设备在线状态，可以作为心跳使用
    obj.check_device_status()

    obj.set_mode(0)  # 设置模式 mode:0：复制triger 1分10 1: 自己产生

    obj.set_pulse_freq(1, 100)  # 设置脉冲频率

    obj.set_pulse_number(1, 100)  # 设置脉冲个数

    obj.set_trig_mode(0)  # 设置触发模式

