from ZW_RF_FE2000 import RF_FE2000, XY_CH, PI_CH, RO_CH
import numpy as np

if __name__ == '__main__':
    obj = RF_FE2000()
    obj.ethernet_connect("127.0.0.1", 8080)

    # PCIE Card1 "XY-1/2/3/4" connect to "B_XY1/2/3/4_1"
    # CH:Freq is 4.2-5.5GHz, GAIN is ≈5dB, the default attenuation is 30dB.
    obj.set_xy_att(XY_CH.B_XY4_2, 31)
    obj.get_xy_att(XY_CH.B_XY4_2)

    # PCIE Card1 "OUT" connect to "B_IN1"
    # CH:Freq is 6.2-7.5GHz, GAIN is ≈5dB, the default attenuation is 30dB.
    obj.set_in_att(PI_CH.B_IN1, 30)
    obj.get_in_att(PI_CH.B_IN1)

    # PCIE Card1 "In" connect to "B_OUT1"
    # CH:Freq is 6.2-7.5GHz, GAIN is ≈55dB, the default attenuation is 60dB.
    obj.set_out_att(RO_CH.B_OUT1, 60)
    obj.get_out_att(RO_CH.B_OUT1)

    obj.set_ip_mask("192.168.1.100", "255.255.255.0")
