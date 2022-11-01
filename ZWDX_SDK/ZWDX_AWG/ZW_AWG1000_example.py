import ZW_AWG1000
import numpy as np

if __name__ == "__main__":
    handle_data = ZW_AWG1000.AWG1000()
    handle_cmd = ZW_AWG1000.AWG1000()

    handle_cmd.connect("192.168.1.100", 9000)
    handle_data.connect("192.168.1.100", 9001)

    # 指令配置各种参数
    handle_cmd.open_channel([1, 2, 3])  # 打开通道

    handle_cmd.close_channel([1, 2, 3])  # 关闭通道

    handle_data.send_waveform_data(np.arange(0, 100, 1), 1)  # 发送波形数据到通道1
    handle_data.send_waveform_file(r"E:\Hw_work\Python\Project\ZW_AWG\xx.dat", 1)  # 发送波形文件到通道1

    handle_cmd.set_refclk("int_ref", 100)  # 设置内外参考

    handle_cmd.set_rf_power(1, 25)  # 通道1设置输出功率25dB

    handle_cmd.set_output_mode(1, "DC")  # 通道1设置DC模式输出

    handle_cmd.set_trigger_param(1, 1, 100, 100)  # 通道1设置触发参数

    handle_cmd.get_temperature()  # 获取温度

    handle_cmd.set_fan_speed(250)  # 设置风扇转速

    handle_cmd.set_data_source(100, 0)  # 设置数据源

    handle_cmd.change_dev_ip("eth", "192.168.1.123")  # 以太网方式设置设备IP

    handle_cmd.open_uart("COM4")  # 打开串口4,备后面获取IP

    handle_cmd.get_dev_ip()  # 从串口获取设备IP

    handle_cmd.set_default_vbias(1, 1.0)  # 设置DA默认输出电压

    handle_cmd.close_uart()  # 关闭串口

    handle_cmd.disconnect()  # 断开连接
    handle_data.disconnect()  # 断开连接
