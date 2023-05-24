from ZW_DC2000_NV_16CH import DC2000

if __name__ == '__main__':
    # 获取设备对象
    obj = DC2000()

    # 连接根据硬件连接方式二选一
    # 以太网方式连接设备
    obj.ethernet_connect("192.168.1.20", 8080)

    # 串口方式连接设备
    obj.uart_connect("COM3")

    # 改变设备IP, 不用重启设备，改变后自动生效
    obj.set_ip_mask("192.168.1.100")

    # 获取设备IP,子网掩码MASK
    ip_info = obj.get_ip_mask()
    print(ip_info)

    # 获取设备IP,子网掩码MASK
    ip_info = obj.get_ip_mask()

    # 设置电压上升/下降斜率,单位mv/s
    obj.set_volt_slope(1000)

    # 安全打开通道
    obj.set_ch_on([8])                                                          # 打开通道8
    obj.set_ch_on([1, 5, 8])                                                    # 打开1,5,8通道
    obj.set_ch_on([0])                                                          # 打开所有通道

    # 获取通道开启状态
    ch8_status = obj.get_ch_status([8])                                         # 获取通道8开关状态
    ch158_status = obj.get_ch_status([1, 5, 8])                                 # 获取通道1,5,8开关状态
    chall_status = obj.get_ch_status([0])                                       # 获取所有通道开关状态

    # 设置电压
    obj.set_vol([8], 5)                                                         # 通道8设置5V电压
    obj.set_vol([1, 5, 8], -5)                                                  # 通道1,5,8设置-5V电压
    obj.set_vol([0], 5)                                                         # 所有通道设置5V电压

    # 获取电压,用户使用
    ch8vol = obj.get_vol([8])                                                   # 获取通道8电压
    ch158vol = obj.get_vol([1, 5, 8])                                           # 获取通道5电压
    challvol = obj.get_vol([0])                                                 # 获取所有通道电压

    # 获取设备温度
    temp = obj.get_temp()       

    # 安全关闭通道
    obj.set_ch_off([8])                                                         # 安全关闭8通道
    obj.set_ch_off([1, 5, 8])                                                   # 安全关闭1,5,8通道
    obj.set_ch_off([0])                                                         # 安全关闭所有通道

    # 使能/禁用通道电流采集功能
    obj.set_bw_option([8], 1)                                                   # 启用通道8BW功能
    obj.set_bw_option([1, 5, 8], 0)                                             # 禁用通道1,5,8BW功能
    obj.set_bw_option([0], 0)                                                   # 禁用所有通道BW功能

    # **************************************内部使用*************************************
    # 内部使用接口，客户不使用
    # 从DAC获取电压,需等待电压正常输出后才能读取,需要延时等待,内部测试使用
    ch1voldac = obj._get_vol_dac([8])                                           # 获取通道8电压
    ch158voldac = obj._get_vol_dac([1, 5, 8])                                   # 获取通道5电压
    challvoldac = obj._get_vol_dac([0])                                         # 获取所有通道电压

    # 快速关闭通道,内部使用，不建议用户使用
    obj._set_ch_off_fast([8])                                                   # 快速关闭8通道
    obj._set_ch_off_fast([1, 5, 8])                                             # 快速关闭1,5,8通道
    obj._set_ch_off_fast([0])                                                   # 快速关闭所有通道

    # 使能/禁用PWM调节精度到2uv
    obj._set_pwm_status([8], 1)                                                 # 使能通道8PWM
    obj._set_pwm_status([1, 5, 8], 0)                                           # 禁用通道1,5,8PWM
    obj._set_pwm_status([0], 1)                                                 # 使能所有通道PWM

    # 设置设备后面复位按钮复位斜率
    obj._set_reset_volt_slop(1000)                                              # 设置复位斜率1000mv/s

    obj._get_bw_current([8])
    obj._set_ch_mode()
    # **********************************************************************************


