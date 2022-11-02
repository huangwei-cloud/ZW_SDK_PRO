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

    # 打开所有通道
    obj.open_all_channels()

    # 关闭所有通道
    obj.close_all_channels()

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

