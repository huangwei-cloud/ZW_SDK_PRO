from ZW_DC1000 import DC1000, COM_CH, COM_STATUS

if __name__ == '__main__':
    # 获取设备对象
    obj = DC1000()

    # 连接根据硬件连接方式二选一
    # 以太网方式连接设备
    obj.ethernet_connect("192.168.1.20", 8080)

    # 串口方式连接设备
    obj.uart_connect("COM3")

    # 设置电压上升/下降斜率
    obj.set_volt_slope(1000)

    # 安全打开通道
    obj.set_ch_on([COM_CH.CH8])                                                         # 打开通道8
    obj.set_ch_on([COM_CH.CH1, COM_CH.CH5, COM_CH.CH8])                                 # 打开1,5,8通道
    obj.set_ch_on([COM_CH.CHALL])                                                       # 打开所有通道

    # 获取通道开启状态
    ch8_status = obj.get_ch_status([COM_CH.CH8])                                        # 获取通道8开关状态
    ch158_status = obj.get_ch_status([COM_CH.CH1, COM_CH.CH5, COM_CH.CH8])              # 获取通道1,5,8开关状态
    chall_status = obj.get_ch_status([COM_CH.CHALL])                                    # 获取所有通道开关状态

    # 设置电压
    obj.set_vol([COM_CH.CH8], 5)                                                        # 通道8设置5V电压
    obj.set_vol([COM_CH.CH1, COM_CH.CH5, COM_CH.CH8], -5)                               # 通道1,5,8设置-5V电压
    obj.set_vol([COM_CH.CHALL], 5)                                                        # 所有通道设置5V电压

    # 获取电压,用户使用
    ch8vol = obj.get_vol([COM_CH.CH8])                                                  # 获取通道8电压
    ch158vol = obj.get_vol([COM_CH.CH1, COM_CH.CH5, COM_CH.CH8])                        # 获取通道5电压
    challvol = obj.get_vol([COM_CH.CHALL])                                              # 获取所有通道电压

    # 从DAC获取电压,需等待电压正常输出后才能读取,需要延时等待,内部测试使用
    ch1voldac = obj._get_vol_dac([COM_CH.CH8])                                          # 获取通道8电压
    ch158voldac = obj._get_vol_dac([COM_CH.CH1, COM_CH.CH5, COM_CH.CH8])                # 获取通道5电压
    challvoldac = obj._get_vol_dac([COM_CH.CHALL])                                      # 获取所有通道电压

    # 使能/禁用通道端接电阻
    obj.set_res_option([COM_CH.CH8], COM_STATUS.ENABLE)                                 # 使能通道8端接电阻
    obj.set_res_option([COM_CH.CH1, COM_CH.CH5, COM_CH.CH8], COM_STATUS.DISABLE)        # 禁用通道1,5,8端接电阻
    obj.set_res_option([COM_CH.CHALL], COM_STATUS.ENABLE)                               # 使能所有通道端接电阻

    # 使能/禁用通道端接电容
    obj.set_cap_option([COM_CH.CH8], COM_STATUS.ENABLE)                                 # 使能通道8端接电容
    obj.set_cap_option([COM_CH.CH1, COM_CH.CH5, COM_CH.CH8], COM_STATUS.DISABLE)        # 禁用通道1,5,8端接电容
    obj.set_cap_option([COM_CH.CHALL], COM_STATUS.ENABLE)                               # 使能所有通道端接电容

    # 使能/禁用通道电流采集功能
    obj.set_iv_option([COM_CH.CH8], COM_STATUS.ENABLE)                                  # 启用通道8电流采集功能
    obj.set_iv_option([COM_CH.CH1, COM_CH.CH5, COM_CH.CH8], COM_STATUS.DISABLE)         # 禁用通道1,5,8电流采集功能
    obj.set_iv_option([COM_CH.CHALL], COM_STATUS.DISABLE)                               # 禁用所有通道电流采集功能

    # 获取通道电流
    ch1a = obj.get_current([COM_CH.CH8])                                                # 获取通道8电流
    ch158a = obj.get_current([COM_CH.CH1, COM_CH.CH5, COM_CH.CH8])                      # 获取通道1,5,8电流
    challa = obj.get_current([COM_CH.CHALL])                                            # 获取所有通道电流

    # 安全关闭通道
    obj.set_ch_off([COM_CH.CH8])                                                        # 安全关闭8通道
    obj.set_ch_off([COM_CH.CH1, COM_CH.CH5, COM_CH.CH8])                                # 安全关闭1,5,8通道
    obj.set_ch_off([COM_CH.CHALL])                                                      # 安全关闭所有通道

    # 快速关闭通道,内部使用，不建议用户使用
    obj._set_ch_off_fast([COM_CH.CH8])                                                  # 快速关闭8通道
    obj._set_ch_off_fast([COM_CH.CH1, COM_CH.CH5, COM_CH.CH8])                          # 快速关闭1,5,8通道
    obj._set_ch_off_fast([COM_CH.CHALL])                                                # 快速关闭所有通道

    # 使能/禁用PWM调节精度到2uv
    obj._set_pwm_status([COM_CH.CH8], COM_STATUS.ENABLE)                                # 使能通道8PWM
    obj._set_pwm_status([COM_CH.CH1, COM_CH.CH5, COM_CH.CH8], COM_STATUS.DISABLE)       # 禁用通道1,5,8PWM
    obj._set_pwm_status([COM_CH.CHALL], COM_STATUS.ENABLE)                              # 使能所有通道PWM

    # 设置设备后面复位按钮复位斜率
    obj._set_reset_volt_slop(1000)                                                      # 设置复位斜率1000mv/s

    # 检测设备在线状态，可以作为心跳使用
    obj._check_device_status()

    # 改变设备IP, 不用重启设备，改变后自动生效
    obj.change_ip("192.168.1.100")


