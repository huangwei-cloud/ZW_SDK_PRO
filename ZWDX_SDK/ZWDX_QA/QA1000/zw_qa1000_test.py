# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 14:17:22 2022

@author: NUC1165G7
"""

import time

from zw_qa1000_driver_20221229 import fpgadev

dev=fpgadev()    
import numpy as np
import qulab_toolbox.wavedata as WD
import matplotlib.pyplot as plt
from IPython.core.pylabtools import figsize # import figsize
import ctypes
from binascii import hexlify
figsize(10, 7) # 设置 figsize
#fig, ax = plt.subplots(1,1)
#ax.set_xticks(ax.get_xticks()[::2])
plt.rcParams['savefig.dpi'] = 100 #图片像素
plt.rcParams['figure.dpi'] = 100 #分辨率
plt.rcParams['font.size'] = 16
plt.rcParams['font.style'] = 'normal'
plt.rcParams['ytick.minor.visible']=False
plt.rcParams['xtick.minor.visible']=False
plt.tick_params(labelsize=16)
plt.close()

#%%
def my_fft_num(adc_data):
    fft_data = np.fft.fft(adc_data)/len(adc_data)

    fft_len = np.uint(len(adc_data)/2)

    fft_data_1 = fft_data[:fft_len]

    fft_abs = np.abs(fft_data_1)
    
    fft_abs1 = fft_abs/np.max(fft_abs)
    de = 1e-5
    fft_db = 20*np.log10(fft_abs1 + de)
    
    plt.figure()
    plt.plot(fft_db)

    fpwr = fft_abs1 * fft_abs1.T
    
    fft_abs_max = np.max(fft_abs1[1:fft_len])
    mmm = np.where(fft_abs1 == fft_abs_max)[0][0]
    
#    nad  = np.sqrt(np.sum(fpwr) - fpwr[0] - np.max(fpwr))
#    nrms = np.sum(fpwr) - fpwr[0] - fpwr[1] - np.max(fpwr) - fpwr[mmm*2] - fpwr[mmm*3]
    nrms = np.sum(fpwr) - fpwr[0] - fpwr[1] - np.max(fpwr)

    nrms = np.sqrt(nrms)

    fft_db = list(fft_db)
    fft_m = np.max(fft_db)
    fft_new = fft_db[:mmm-10]+fft_db[mmm+10:-1]

    print('sfdr : ',fft_m - np.max(fft_new))

#    sinad = 20 * np.log10(np.max(fft_abs1)/nad)
#    print('sinad : ',sinad)
    snr = 20 * np.log10(np.max(fft_abs1)/nrms)
    print('snr : ',snr)
    
    enob = (snr - 1.76)/6.02
    
    print('enob : ',enob)
    
    return 'ok'
#%%
dev.rfdac_SetNyquistZone(0)
#dev.rfadc_SetNyquistZone(1)
#dev.rfdac_SetDecoderMode(0)
#dev.rfadc_SetCalibrationMode(0)
#dev.rfdac_SetDACVOP(1)
#dev.rfadc_SetDSA(6)
#dev.rfadc_SetDither(0)

#%%data len max 2.62144e-05

sampleRate=8e9

fs_fout = sampleRate/256/1024

fout = 5812e6

fout = fout//fs_fout*fs_fout # dac_data_continue
datalen = 256*1024/sampleRate
#datalen = 256/sampleRate

sin1=WD.Sin(fout*2*np.pi,0,datalen,sampleRate)*(2**13-1)
dac_data = np.int16(sin1.data)
#sin1 = range(256*1024)

#dac_data = np.int16(sin1)
#plt.figure()
#plt.plot(dac_data)

#chennel_num = 0
#slot = dev.da_ch[chennel_num][0]
#ch_num = dev.da_ch[chennel_num][1]

trigger_delay = 0
replay_times = 10000000
replay_continue = 1

chennel_num = 0
#dev.trigger_close()
#for chennel_num in range(6):
#    dev.dac_updata(chennel_num+6,trigger_delay,replay_times,replay_continue,dac_data)
dev.dac_updata(chennel_num,trigger_delay,replay_times,replay_continue,dac_data)
#dev.dac_close()
#chennel_num = 12
#dev.dac_updata(chennel_num,trigger_delay,replay_times,replay_continue,dac_data)

trigger_source = 0
trigger_us = 600
trigger_num = 10
trigger_continue = 0
dev.trigger_ctrl(trigger_source,trigger_us,trigger_num,trigger_continue)

#%%
#dev.rfadc_SetNyquistZone(1)
dev.rfadc_SetCalibrationMode(1)
#dev.rfadc_SetDither(0)

#%%
#采集ADC原始数据-刷新
adc_chennel_num = 1
trigger_delay = 0
times = 1
save_len = 2**15
trigger_source = 0
trigger_us = 600
trigger_num = 10
trigger_continue = 0
dev.trigger_close()

for adc_chennel_num in range(12):
    dev.rd_adc_data_ctrl(adc_chennel_num,trigger_delay,times,save_len)


dev.trigger_ctrl(trigger_source,trigger_us,times,trigger_continue)

time.sleep(0.1)
adc_data = []
while 1:
    adc_data_buf,save_len = dev.rd_adc_data(0,times,save_len)
    if save_len != -1:
        break

adc_data.append(adc_data_buf)

for adc_chennel_num in range(11):
    adc_data_buf,save_len_i = dev.rd_adc_data(adc_chennel_num+1,times,save_len)
    adc_data.append(adc_data_buf)


adc_chennel_num = 0
plt.figure()
#for adc_chennel_num in range(16):
#    plt.plot(adc_data[adc_chennel_num][500:600])
#plt.figure()
#adc_chennel_num = 1
plt.plot(adc_data[adc_chennel_num])  

#绘制某一个通道ADC采集数据FFT波形

    
adc_data_w = []
data_w = np.kaiser(save_len,8)
adc_data_w = adc_data[adc_chennel_num]/times
adc_data_w = adc_data_w*data_w
#
fft_data = []
fft_data = (20*np.log10(abs(np.fft.fft(adc_data_w))))
my_fft_num(adc_data_w)
#plt.figure()
#plt.plot(fft_data[0:save_len//2])

#%%
#绘制所有通道ADC采集数据FFT波形
fft_data = []
for adc_chennel_num in range(8):
    fft_data.append(20*np.log10(abs(np.fft.fft(adc_data[adc_chennel_num]/times))))

for adc_chennel_num in range(8):
    plt.figure()
    plt.plot(fft_data[adc_chennel_num])

#%%data len max 2.62144e-05

sampleRate=8e9

fs_fout = sampleRate/256/1024

fout = 5812e6

fout = fout//fs_fout*fs_fout # dac_data_continue
datalen = 256*1024/sampleRate
#datalen = 256/sampleRate

sin1=WD.Sin(fout*2*np.pi,0,datalen,sampleRate)*(2**13-1)
dac_data = np.int16(sin1.data)
#sin1 = range(256*1024)

#dac_data = np.int16(sin1)
#plt.figure()
#plt.plot(dac_data)

#chennel_num = 0
#slot = dev.da_ch[chennel_num][0]
#ch_num = dev.da_ch[chennel_num][1]

trigger_delay = 0
replay_times = 10000000
replay_continue = 0

chennel_num = 0
#dev.trigger_close()
#for chennel_num in range(6):
#    dev.dac_updata(chennel_num+6,trigger_delay,replay_times,replay_continue,dac_data)
dev.dac_updata(chennel_num,trigger_delay,replay_times,replay_continue,dac_data)
#dev.dac_close()
#chennel_num = 12
#dev.dac_updata(chennel_num,trigger_delay,replay_times,replay_continue,dac_data)

#trigger_source = 0
#trigger_us = 600
#trigger_num = 10
#trigger_continue = 0
#dev.trigger_ctrl(trigger_source,trigger_us,trigger_num,trigger_continue)

#%%

adc_chennel_num = 0
trigger_delay = 490
times = 1000

mul_f = []

mul_start_phase = 0

mul_f_phase = 5812e6

mul_f_len = 2**15

for i in range(25):
    mul_f_i = []
    mul_start_phase = 2*np.pi/25*i
    mul_f_i.append(mul_start_phase)
    mul_f_i.append(mul_f_phase)
    mul_f_i.append(mul_f_len)
    mul_f.append(mul_f_i)

dev.trigger_close()

#for adc_chennel_num in range(12):
#    dev.rd_adc_mul_data_ctrl(adc_chennel_num,trigger_delay,times,mul_f)

dev.rd_adc_mul_data_ctrl(adc_chennel_num,trigger_delay,times,mul_f)
 
time.sleep(0.5)
trigger_source = 0
trigger_us = 500
trigger_num = 1000
trigger_continue = 0
dev.trigger_ctrl(trigger_source,trigger_us,trigger_num,trigger_continue)

time.sleep(0.1)
mul_data = []
mul_data_i = []
for modle_num in range(25):

    while 1:
        mul_data_bufe,read_data_len = dev.rd_adc_mul_data(adc_chennel_num,modle_num,times)
        if read_data_len != -1:
            break
    mul_data_i.append(mul_data_bufe)
mul_data.append(mul_data_i)
#for adc_chennel_num in range(7):
#    mul_data_bufe,read_data_len = dev.rd_adc_mul_data(adc_chennel_num+1,modle_num,times)
#    mul_data.append(mul_data_bufe)

#for adc_chennel_num in range(7,8):
#    plt.figure()
#    for i in range(25):
#        plt.plot(mul_data[adc_chennel_num][i].real/mul_f_len/2**13,mul_data[adc_chennel_num][i].imag/mul_f_len/2**13,'.')
        
plt.figure()
for i in range(25):
    plt.plot(mul_data[0][i].real/mul_f_len/2**13,mul_data[0][i].imag/mul_f_len/2**13,'.')


#%%生成连续波信号
#dev.rfdac_SetNyquistZone(1)
#dev.rfdac_SetDecoderMode(0)
#dev.rfdac_SetDACVOP(0.5)

sampleRate=8e9

fs_fout = sampleRate/256/1024

fout = 7812e6

fout_wr = fout//fs_fout*fs_fout # dac_data_continue
datalen = 256*1024/sampleRate

sin1=WD.Sin(fout_wr*2*np.pi,0,datalen,sampleRate)*(2**13-1)
fout = fout + 100e6
#sin1=WD.Sin(fout*2*np.pi,0,datalen,sampleRate)*0

dac_data = np.int16(sin1.data)

#plt.figure()
#plt.plot(dac_data)
#fft_data = []
#fft_data = (abs(np.fft.fft(dac_data)))
#
#plt.plot(fft_data[0:256*1024//2])

#chennel_num = 0
#slot = dev.da_ch[chennel_num][0]
#ch_num = dev.da_ch[chennel_num][1]

trigger_delay = 0
replay_times = 100000
replay_continue = 1

#for i in range(12):
#    dev.dac_close(i)
#    dev.dac_ch_ctrl('slot0',i,0,0,0,0,0)
dev.trigger_close()
#chennel_num = 11
#dev.dac_updata(chennel_num,trigger_delay,replay_times,replay_continue,dac_data)
for chennel_num in range(12):
    dev.dac_updata(11-chennel_num,trigger_delay,replay_times,replay_continue,dac_data)

#i=0
#dev.BoardInfo[str(i)][1]
#dev.da_ch

trigger_source = 1
trigger_us = 500
trigger_num = 10
trigger_continue = 0
dev.trigger_ctrl(trigger_source,trigger_us,trigger_num,trigger_continue)    
#%%

adc_chennel_num = 0
trigger_delay = 0
times = 1
save_len = 2**15-1

dev.trigger_close()


dev.rd_adc_data_ctrl(adc_chennel_num,trigger_delay,times,save_len)

dev.rd_adc_data_ctrl(4,trigger_delay,times,save_len)

mul_f = []

mul_start_phase = 0
mul_f_phase = 5100e6
mul_f_len = 2**15-1

for i in range(25):
    mul_f_i = []
    mul_start_phase = 2*np.pi/25*i
    mul_f_i.append(mul_start_phase)
    mul_f_i.append(mul_f_phase)
    mul_f_i.append(mul_f_len)

    mul_f.append(mul_f_i)

dev.rd_adc_mul_data_ctrl(adc_chennel_num,trigger_delay,times,mul_f)

dev.trigger_ctrl(trigger_source,trigger_us,times,trigger_continue)

time.sleep(0.1)
adc_data = []
while 1:
    adc_data_buf,save_len = dev.rd_adc_data(adc_chennel_num,times,save_len)
    if save_len != -1:
        break
adc_data.append(adc_data_buf)


mul_data = []
for modle_num in range(25):

    while 1:
        mul_data_bufe,read_data_len = dev.rd_adc_mul_data(adc_chennel_num,modle_num,times)
        if read_data_len != -1:
            break
    mul_data.append(mul_data_bufe)


sampleRate=2.5e9

fout = 5100e6

datalen = save_len/sampleRate

#cos_data=WD.Cos(fout*2*np.pi,0,datalen,sampleRate)*(2**17)
#sin_data=WD.Sin(fout*2*np.pi,0,datalen,sampleRate)*(2**17)
#adc_data_mul_i = (np.int32(cos_data.data) + np.int32(sin_data.data)*1j)

tlist = np.arange(save_len)*2*np.pi*fout/sampleRate
cos_data = np.int32(np.cos(tlist)*(2**17-1))
sin_data = np.int32(np.sin(tlist)*(2**17-1))

adc_data_mul_i = (cos_data + sin_data*1j)

adc_data_mul = sum(adc_data_mul_i.real*adc_data[0])+sum(adc_data_mul_i.imag*adc_data[0])*1j
#%%
plt.figure()
for i in range(25):
    plt.plot(mul_data[i].real/mul_f_len/2**13,mul_data[i].imag/mul_f_len/2**13,'.')
plt.plot(adc_data_mul.real/mul_f_len/2**13,adc_data_mul.imag/mul_f_len/2**13,'.')
plt.plot(mul_data[1].real/mul_f_len/2**13,mul_data[1].imag/mul_f_len/2**13,'.')

#%%
point_num = 12

print(cos_data[point_num])

#abs(adc_data_mul)
#abs(mul_data[0])
#%%
plt.figure()
plt.plot(sin_data)


#%%
sampling = 0
dev.system_sampling(sampling=sampling,step=0,self_set=1)
#for i in range(len(dev.da_ch)):
#    dev.dac_Nyquist_cfg(chennel_num=i,Nyquist=1)


#%%test delay
plt.close(fig0)
plt.close(fig1)
plt.close(fig2)
plt.close(fig3)
plt.close(fig4)

bord_n = 2


trigger_source = 0
trigger_us = 500
trigger_times = 10
trigger_continue = 0

dev.trigger_close()
time0 = time.time()

save_len = 16384*32#25600

modle_en = 1
adc_trigger_delay = 0
trigger_times_s = 10

for adc_ch in range(len(dev.ad_ch)):
#for adc_ch in range(1):
    dev.adc_modle_reset(adc_ch,1)
    dev.rd_adc_data_ctrl(adc_ch,modle_en,adc_trigger_delay,trigger_times_s,save_len)
    dev.adc_modle_reset(adc_ch,0)

time1 = time.time()
dev.trigger_ctrl(trigger_source,trigger_us,trigger_times,trigger_continue)


#time.sleep(0.5)
adc_data_s = []
for adc_ch in range(len(dev.ad_ch)):
#for adc_ch in range(1):
    while 1:
        adc_data_bufe,data_len = dev.rd_adc_data(adc_ch,trigger_times_s,save_len)
        if data_len != -1:
            break
    adc_data_s.append(adc_data_bufe)

time2 = time.time()

adc_board = 0
time_cn = 0

#fig0 = plt.figure()
##plt.plot(adc_data_s[adc_board][time_cn][:50])
#for adc_ch in range(4):
##    plt.plot(adc_data_s[adc_ch][time_cn][:50])
#    plt.plot(adc_data_s[adc_ch][time_cn])
#    

fig0 = plt.figure()
plt.plot(adc_data_s[(bord_n*4+4)%12][time_cn][:20])
plt.plot(adc_data_s[(bord_n*4+8)%12][time_cn][:20])
for adc_ch in range(4):
    plt.plot(adc_data_s[adc_ch+bord_n*4][time_cn][:20])

fig1 = plt.figure()
for i in range(trigger_times):
    adc_data_fft = 20*np.log10(abs(np.fft.fft(adc_data_s[0+bord_n*4][i])))
    adc_data_fft = adc_data_fft - max(adc_data_fft)
    plt.plot(adc_data_fft[1:save_len//2])
fig2 = plt.figure()
for i in range(trigger_times):
    adc_data_fft = 20*np.log10(abs(np.fft.fft(adc_data_s[1+bord_n*4][i])))
    adc_data_fft = adc_data_fft - max(adc_data_fft)
    plt.plot(adc_data_fft[1:save_len//2])
fig3 = plt.figure()
for i in range(trigger_times):
    adc_data_fft = 20*np.log10(abs(np.fft.fft(adc_data_s[2+bord_n*4][i])))
    adc_data_fft = adc_data_fft - max(adc_data_fft)
    plt.plot(adc_data_fft[1:save_len//2])
fig4 = plt.figure()
for i in range(trigger_times):
    adc_data_fft = 20*np.log10(abs(np.fft.fft(adc_data_s[3+bord_n*4][i])))
    adc_data_fft = adc_data_fft - max(adc_data_fft)
    plt.plot(adc_data_fft[1:save_len//2])


    
print(time1-time0)
print(time2-time1 - trigger_us*1e-6*trigger_times_s)
#%%adc fft test

adc_ch = 0

trigger_source = 0
trigger_us = 500
trigger_times = 1
trigger_continue = 0

dev.trigger_close()

save_len = 16384*64#25600

modle_en = 1
adc_trigger_delay = 0
trigger_times_s = 1

dev.adc_modle_reset(adc_ch,1)
dev.rd_adc_data_ctrl(adc_ch,modle_en,adc_trigger_delay,trigger_times_s,save_len)
dev.adc_modle_reset(adc_ch,0)

dev.trigger_ctrl(trigger_source,trigger_us,trigger_times,trigger_continue)

adc_data_s = []
while 1:
    adc_data_bufe,data_len = dev.rd_adc_data(adc_ch,trigger_times_s,save_len)
    if data_len != -1:
        break
adc_data_s.append(adc_data_bufe)

#plt.figure()
#plt.plot(adc_data_s[0][0])
print('amp:',(max(adc_data_s[0][0]) - min(adc_data_s[0][0]))/2**14)
my_fft_num(adc_data_s[0][0])

#%%
slot = 'slot0'
sampleRate = 5e9
fin = 101e6
data_len = 25600
start_addr = 0
chennel_num = 0
data_wr = []
#sin1=WD.Sin(fin*2*np.pi,0,datanum/sampleRate,sampleRate)*(2**15-1)
#dac_data.append(sin1.data)
time0 = time.time()
data_wr.append(np.arange(data_len))
time1 = time.time()
print(time1-time0)

time2 = time.time()
dev.pcie_wr_data(slot,chennel_num,start_addr,data_wr[0])
time3 = time.time()
data_rd = dev.pcie_rd_data(slot,chennel_num,start_addr,data_len,1)
time4 = time.time()
print(time3-time2)
print(time4-time3)
print(time4-time2)


plt.figure()
plt.plot(data_rd[0])

#%%


adc_reg_addr = 0x400+22*4+1
dac_ctrl_reg = 0x55223311
dev.writeReg(adc_reg_addr,dac_ctrl_reg,slot)

print(hex(dev.readReg(adc_reg_addr,slot)))

#%%
chennel_num = 0
data_len = 2**10+500
data = np.int16(np.arange(data_len))

pcie_dma_wr_len = 2**15

data_len = np.ceil(len(data)/pcie_dma_wr_len).astype(int)*pcie_dma_wr_len

data_wr_bufe = np.zeros(data_len)
data_wr_bufe[:len(data)] = data

data_wr_bufe = np.reshape(data_wr_bufe,(data_len//pcie_dma_wr_len,pcie_dma_wr_len))

pbuf = ctypes.create_string_buffer(pcie_dma_wr_len*2)
for i in range(len(data_wr_bufe)):
#            data_wr_bufe_i = np.int16(data_wr_bufe[i])
#            data_wr_bufe_i = ctypes.cast(data_wr_bufe_i.ctypes.data, ctypes.POINTER(ctypes.c_short))

    pbuf.raw = np.int16(data_wr_bufe[i])

    data_wr_bufe_i = ctypes.cast(ctypes.addressof(pbuf), ctypes.POINTER(ctypes.c_short))

    dev.fpga_dma_write_bysize(slot,0x11000000+0x20000*chennel_num,data_wr_bufe_i,pcie_dma_wr_len*2)

#%%
    
slot = 'slot0'

trigger_source = 0
trigger_us = 500
trigger_times = 10
trigger_continue = 0

dev.trigger_close()
time0 = time.time()

save_len = 16384*32#25600

modle_en = 1
adc_trigger_delay = 0
trigger_times_s = 10

for adc_ch in range(len(dev.ad_ch)):
#for adc_ch in range(1):
    dev.adc_modle_reset(adc_ch,1)
    dev.rd_adc_data_ctrl(adc_ch,modle_en,adc_trigger_delay,trigger_times_s,save_len)
    dev.adc_modle_reset(adc_ch,0)

time1 = time.time()
dev.trigger_ctrl(trigger_source,trigger_us,trigger_times,trigger_continue)


#time.sleep(0.5)
adc_data_s = []
for adc_ch in range(len(dev.ad_ch)):
#for adc_ch in range(1):
    while 1:
        adc_data_bufe,data_len = dev.rd_adc_data(adc_ch,trigger_times_s,save_len)
        if data_len != -1:
            break
    adc_data_s.append(adc_data_bufe)

time2 = time.time()

adc_board = 0
time_cn = 0
fig = plt.figure()
#plt.plot(adc_data_s[adc_board][time_cn][:50])
for adc_ch in range(len(dev.ad_ch)):
    plt.plot(adc_data_s[adc_ch][time_cn][:50])
#    plt.plot(adc_data_s[adc_ch][time_cn])
    
plt.figure()
for adc_ch in range(len(dev.ad_ch)):
    adc_data_fft = 20*np.log10(abs(np.fft.fft(adc_data_s[adc_ch][time_cn])))
    adc_data_fft = adc_data_fft - max(adc_data_fft)
    plt.plot(adc_data_fft[1:save_len//2])
    
print(time1-time0)
print(time2-time1 - trigger_us*1e-6*trigger_times_s)
#%%
adc_board = 2
time_cn = 0


fig = plt.figure()
for adc_ch in range(4):
    plt.plot(adc_data_s[adc_board*4 + adc_ch][time_cn][:50])
plt.figure()

for adc_ch in range(4):
    adc_data_fft = 20*np.log10(abs(np.fft.fft(adc_data_s[adc_board*4 + adc_ch][time_cn])))
    adc_data_fft = adc_data_fft - max(adc_data_fft)
    plt.plot(adc_data_fft[1:save_len//2])

#%%
adc_ch = 4


fig = plt.figure()
#plt.plot(adc_data_s[adc_ch][time_cn][:50])
plt.plot(adc_data_s[adc_ch][time_cn])
plt.figure()
adc_data_fft = 20*np.log10(abs(np.fft.fft(adc_data_s[adc_ch][time_cn])))
adc_data_fft = adc_data_fft - max(adc_data_fft)
plt.plot(adc_data_fft[1:save_len//2])
#%%
    
adc_board = 11
time_cn = 0
fig = plt.figure()
plt.plot(adc_data_s[adc_board][time_cn])
plt.figure()
adc_data_fft = 20*np.log10(abs(np.fft.fft(adc_data_s[adc_board][time_cn])))
adc_data_fft = adc_data_fft - max(adc_data_fft)
plt.plot(adc_data_fft[1:save_len//2])

#%%

point_add = 47
hex(0xfffff+adc_data_bufe[0][25840+point_add]+1)


#%%

slot = 'slot0'

sampling = 0

trigger_source = 0
trigger_us = 50
trigger_times = 10000
trigger_continue = 0


save_len = 16384
adc_ch = 0
modle_en = 1
adc_trigger_delay = 0
trigger_times_s = 10000


dev.trigger_close()
if sampling == 0:
    sampleRate=5e9
    adc_trigger_delay = 700
    fout = 1300e6
elif sampling == 1:
    sampleRate=4e9
    adc_trigger_delay = 700
    fout = 100e6
    
sin1=WD.Sin(fout*2*np.pi,0,200e-6,sampleRate/2)*(2**13-1)
cos1=WD.Cos(fout*2*np.pi,0,200e-6,sampleRate/2)*(2**13-1)

sin_data = np.int16(sin1.data)[:16384]
cos_data = np.int16(cos1.data)[:16384]


data_bufe = []
data_bufe.append(cos_data)
data_bufe.append(sin_data)


time0 = time.time()

#dev.adc_modle_reset(adc_ch,1)


for i in range(20):
    dev.adc_mul_data_wr(adc_ch,i,data_bufe)
    
#dev.adc_modle_reset(adc_ch,0)
time1 = time.time()





dev.adc_modle_reset(adc_ch,1)
dev.rd_adc_data_ctrl(adc_ch,modle_en,adc_trigger_delay,trigger_times_s,save_len)
for i in range(20):
    dev.rd_adc_mul_data_ctrl(adc_ch,modle_en,i,adc_trigger_delay,trigger_times_s,save_len)
dev.adc_modle_reset(adc_ch,0)
#
time2 = time.time()
#time.sleep(0.5)

dev.trigger_ctrl(trigger_source,trigger_us,trigger_times,trigger_continue)


####################################read adc mul data#########################
adc_muldata = []

#time.sleep(0.5)

while 1:
    adc_data_bufe,data_len = dev.rd_adc_mul_data(adc_ch,0,trigger_times_s)

    if data_len != -1:
        break

time3 = time.time()

#    
for i in range(20):
    while 1:
        adc_data_bufe,data_len = dev.rd_adc_mul_data(adc_ch,i,trigger_times_s)
    
        if data_len != -1:
            break
        
    adc_muldata.append(adc_data_bufe)


time4 = time.time()

adc_data_s = []

while 1:
    adc_data_bufe,data_len = dev.rd_adc_data(adc_ch,trigger_times_s,save_len)
    if data_len != -1:
        break
adc_data_s.append(adc_data_bufe)

time5 = time.time()
fig = plt.figure()

for i in range(20):
    plt.plot(adc_muldata[i].real/save_len/2**13,adc_muldata[i].imag/save_len/2**13,'.')


#time_iii = 0

#for i in range(20):
#    plt.plot(adc_muldata[i][time_iii].real/save_len/2**13,adc_muldata[i][time_iii].imag/save_len/2**13,'.')
#time_iii += 1

print('write mul data:',time1-time0)
print('set ctrl reg:',time2-time1)
print('read mul result:',time4-time3)
print('read adc data:',time5-time4)
#adc_data_bufe,data_len,data_test = dev.rd_adc_mul_data(adc_ch,0,trigger_times_s)
#fig = plt.figure()
#plt.plot(adc_data_bufe.real/save_len/2**13,adc_data_bufe.imag/save_len/2**13,'.')

#%%

slot = 'slot0'

sampling = 1

trigger_source = 0
trigger_us = 50
trigger_times = 1024
trigger_continue = 0

mul_data_wr_len = 16384
save_len = 16384
adc_ch = 0
modle_en = 1
adc_trigger_delay = 0
trigger_times_s = 1024


dev.trigger_close()
if sampling == 0:
    sampleRate=5e9
    adc_trigger_delay = 700
    fout = 1300e6
elif sampling == 1:
    sampleRate=4e9
    adc_trigger_delay = 700
    fout = 100e6
    
sin1=WD.Sin(fout*2*np.pi,0,mul_data_wr_len*2/sampleRate,sampleRate/2)*(2**13-1)
cos1=WD.Cos(fout*2*np.pi,0,mul_data_wr_len*2/sampleRate,sampleRate/2)*(2**13-1)

sin_data = np.int16(sin1.data)[:mul_data_wr_len]
cos_data = np.int16(cos1.data)[:mul_data_wr_len]


data_bufe = []
data_bufe.append(cos_data)
data_bufe.append(sin_data)


time0 = time.time()

#dev.adc_modle_reset(adc_ch,1)

for adc_ch in range(len(dev.ad_ch)):
    for i in range(20):
        dev.adc_mul_data_wr(adc_ch,i,data_bufe)
    
#dev.adc_modle_reset(adc_ch,0)
time1 = time.time()




for adc_ch in range(len(dev.ad_ch)):
    dev.adc_modle_reset(adc_ch,1)
    dev.rd_adc_data_ctrl(adc_ch,modle_en,adc_trigger_delay,trigger_times_s,save_len)
    for i in range(20):
        dev.rd_adc_mul_data_ctrl(adc_ch,modle_en,i,adc_trigger_delay,trigger_times_s,save_len)
    dev.adc_modle_reset(adc_ch,0)

time2 = time.time()
#time.sleep(0.5)

dev.trigger_ctrl(trigger_source,trigger_us,trigger_times,trigger_continue)


####################################read adc mul data#########################
adc_muldata = []

#time.sleep(0.5)

while 1:
    adc_data_bufe,data_len = dev.rd_adc_mul_data(adc_ch,0,trigger_times_s)

    if data_len != -1:
        break

time3 = time.time()

#   

for adc_ch in range(len(dev.ad_ch)):
    adc_muldata_i = []
    for i in range(20):
        while 1:
            adc_data_bufe,data_mul_len = dev.rd_adc_mul_data(adc_ch,i,trigger_times_s)
        
            if data_len != -1:
                break
            
        adc_muldata_i.append(adc_data_bufe)
    adc_muldata.append(adc_muldata_i)


time4 = time.time()

adc_data_s = []
for adc_ch in range(len(dev.ad_ch)):
    while 1:
        adc_data_bufe,data_len = dev.rd_adc_data(adc_ch,trigger_times_s,save_len)
        if data_len != -1:
            break
    adc_data_s.append(adc_data_bufe)

time5 = time.time()

replay_times = 2
fig = plt.figure()
for adc_ch in range(len(dev.ad_ch)):
    plt.plot(adc_data_s[adc_ch][replay_times][:50])
    
fig = plt.figure()
for adc_ch in range(len(dev.ad_ch)):
    plt.plot(adc_muldata[adc_ch][0].real/save_len/2**13,adc_muldata[adc_ch][0].imag/save_len/2**13,'.')


#for adc_ch in range(len(dev.ad_ch)):
#    fig = plt.figure()
#    for i in range(20):
#        plt.plot(adc_muldata[adc_ch][i].real/save_len/2**13,adc_muldata[adc_ch][i].imag/save_len/2**13,'.')
#for adc_ch in range(4):
#    plt.plot(adc_muldata[adc_ch][0].real/save_len/2**13,adc_muldata[adc_ch][0].imag/save_len/2**13,'.')



#time_iii = 0

#for i in range(20):
#    plt.plot(adc_muldata[i][time_iii].real/save_len/2**13,adc_muldata[i][time_iii].imag/save_len/2**13,'.')
#time_iii += 1

print('write mul data:',time1-time0)
print('set ctrl reg:',time2-time1)
print('read mul result:',time4-time3)
print('read adc data:',time5-time4)
#adc_data_bufe,data_len,data_test = dev.rd_adc_mul_data(adc_ch,0,trigger_times_s)
#fig = plt.figure()
#plt.plot(adc_data_bufe.real/save_len/2**13,adc_data_bufe.imag/save_len/2**13,'.')
#%%
save_len = 16384
data_mul = cos_data + 1j*sin_data
adc_data_mulii = []

for i in range(trigger_times_s):
    adc_data_mulii.append(sum(data_mul*adc_data_s[0][i]))

adc_data_mulii = np.array(adc_data_mulii)

#fig = plt.figure()

plt.plot(adc_data_mulii.real/save_len/2**13,adc_data_mulii.imag/save_len/2**13,'.')

#%%
mul_times = 7
for i in range(20):
    if adc_muldata[i][mul_times].real < 0:
        adc_muldata_real = 0xffffffff + adc_muldata[i][mul_times].real + 1
    else:
        adc_muldata_real = adc_muldata[i][mul_times].real
    if adc_muldata[i][mul_times].imag < 0:
        adc_muldata_imag = 0xffffffff + adc_muldata[i][mul_times].imag + 1
    else:
        adc_muldata_imag = adc_muldata[i][mul_times].imag
        
    print(hex(np.int64(adc_muldata_real)),hex(np.int64(adc_muldata_imag)))
#    print(hex(np.int64(adc_muldata[i][mul_times].real)),hex(np.int64(adc_muldata[i][mul_times].imag)))
#    print(adc_muldata[i][mul_times].real/save_len/2**13,adc_muldata[i][mul_times].imag/save_len/2**13)

#%%
import serial
serialport = serial.Serial()  #/dev/ttyUSB0
serialport.port = 'COM4'
serialport.baudrate = 115200
serialport.bytesize = 8
serialport.parity = serial.PARITY_NONE
serialport.stopbits = 1
serialport.timeout = 0.5
serialport.open()

#%%
#dev.trigger_ctrl(trigger_source=0,trigger_us=500,trigger_num=1,trigger_continue=1)
fband_data_buf=[]
fband_data_buf.append(np.uint8(0xaa))
fband_data_buf.append(np.uint8(0x01))
fband_data_buf.append(np.uint8(0x1))
fband_data_buf.append(np.uint8(0))
for i in range(28):
    fband_data_buf.append(np.uint8(0x00))


fband_data_buf = bytes(fband_data_buf)
serialport.reset_input_buffer()
serialport.write(fband_data_buf)
time.sleep(0.2)
recv_data = serialport.read_all()
print(recv_data)
#dev.serial_send_cmd(fband_data_buf)
#dev.pcie_serial_send_cmd(1,fband_data_buf)
#
#dev.pcie_serial_reset_input_buffer(slot)
#dev.pcie_serial_write(fband_data_buf,slot)
##time.sleep(0.05)
#recv_data = dev.pcie_serial_read(slot,0.5)
#print(len(recv_data),recv_data)
#dev.pcie_serial_send_cmd(slot,fband_data_buf)


#%%
trigger_source = 0
trigger_us = 500
trigger_times = 1
trigger_continue = 0


chennel_num = 0
data_len = 2505
data_wr = []
data_wr.append(np.arange(data_len)+1)


trigger_delay = 0
replay_cnt = 1
replay_continue_flag = 1
data_point = []
data_point_i = [0,0,trigger_delay,replay_cnt,replay_continue_flag]
data_point.append(data_point_i)

dev.trigger_close()
time0 = time.time()
dev.dac_updata(chennel_num,data_wr[0])
dev.dac_point_updata(chennel_num,data_point)

time1 = time.time()

print(time1-time0)

time.sleep(0.1)
dev.trigger_ctrl(trigger_source,trigger_us,trigger_times,trigger_continue)



#%%continue
sampling = 0
trigger_source = 0
trigger_us = 500
trigger_times = 1
trigger_continue = 0
###############################system sampling confige#########################
time_start = time.time()
chennel_num = 0


dev.trigger_close()
dev.system_sampling(sampling=sampling,step=0,self_set=1)
for i in range(len(dev.da_ch)):
    dev.dac_Nyquist_cfg(chennel_num=i,Nyquist=1)

#generate data

dac_data = []

if sampling == 0:
    sampleRate=5e9
elif sampling == 1:
    sampleRate=4e9
fout = 1250e6


fin = fout
datanum = int(fin/1e6*(sampleRate*1e-6))
sin1=WD.Sin(fin*2*np.pi,0,datanum/sampleRate,sampleRate)*(2**15-1)
dac_data.append(np.int16(sin1.data)[:datanum])


#generate point
replay_num = 0
trigger_delay = 0
replay_cnt = 1
replay_continue_flag = 1

data_point = []
data_point_i = [0,0,trigger_delay,replay_cnt,replay_continue_flag]
data_point.append(data_point_i)



dev.trigger_close()
time0 = time.time()
#chennel_num = 3
#dev.dac_updata(chennel_num,dac_data[0])
#dev.dac_point_updata(chennel_num,data_point)
for chennel_num in range(len(dev.da_ch)):
    dev.dac_updata(chennel_num,dac_data[0])
    dev.dac_point_updata(chennel_num,data_point)

time1 = time.time()

print(time1-time0)

#time.sleep(0.1)
dev.trigger_ctrl(trigger_source,trigger_us,trigger_times,trigger_continue)

#%%continue隔离度

sampling = 1
trigger_us = 500
trigger_continue = 1
trigger_times = 1
###############################system sampling confige#########################
time_start = time.time()



dev.trigger_close()
dev.system_sampling(sampling=sampling,step=0,self_set=1)

for i in range(len(dev.da_ch)):
    dev.dac_Nyquist_cfg(i,1)


#generate data



if sampling == 0:
    sampleRate=5e9
    fout = 271e6
elif sampling == 1:
    sampleRate=4e9
    fout = 271e6


dac_data = []
for i in range(len(dev.da_ch)):
    fin = fout + i*100e6
    datanum = fin/1e6*(sampleRate*1e-6)
    print(datanum/sampleRate)
    sin1=WD.Sin(fin*2*np.pi,0,datanum/sampleRate,sampleRate)*(2**15-1)
    dac_data.append(np.int16(sin1.data))


#generate point
replay_num = 0
trigger_delay = 0
replay_cnt = 1
replay_continue_flag = 1

data_point = []
data_point_i = [0,0,trigger_delay,replay_cnt,replay_continue_flag]
data_point.append(data_point_i)



dev.trigger_close()


time0 = time.time()
#for i in range(len(dev.dev_id.da)):
#    dev.dac_updata(i,dac_data[i])
#    dev.dac_point_updata(i,data_point)


start_ch = 4
for i in range(len(dev.da_ch)):
    dev.dac_updata(start_ch,dac_data[i])
    dev.dac_point_updata(start_ch,data_point)
    start_ch += 1
    if start_ch == 12:
        start_ch = 0
#dev.dac_updata(0,dac_data[0])
#dev.dac_point_updata(0,data_point)
time1 = time.time()

print(time1-time0)

time.sleep(0.1)
dev.trigger_ctrl(0,trigger_us,trigger_times,trigger_continue)

#%%
test_times = 0

#%%short
sampling = 1
trigger_source = 0
trigger_us = 500
trigger_times = 1
trigger_continue = 1
###############################system sampling confige#########################
time_start = time.time()
chennel_num = 0


dev.trigger_close()
dev.system_sampling(sampling=sampling,step=0,self_set=1)
for i in range(12):
    dev.dac_Nyquist_cfg(chennel_num=i,Nyquist=0)

#generate data

dac_data = []

if sampling == 0:
    sampleRate=5e9
elif sampling == 1:
    sampleRate=4e9
fout = 1201e6


fin = fout

sin1=WD.Sin(fin*2*np.pi,0,10e-6,sampleRate)*(2**15-1)
dac_data.append(np.int16(sin1.data))


#generate point
replay_num = 0
trigger_delay = 0
replay_cnt = 1
replay_continue_flag = 0

data_point = []
data_point_i = [0,0,trigger_delay,replay_cnt,replay_continue_flag]
data_point.append(data_point_i)



dev.trigger_close()
time0 = time.time()
for chennel_num in range(len(dev.da_ch)):
    dev.dac_updata(chennel_num,dac_data[0])
    dev.dac_point_updata(chennel_num,data_point)
#dev.dac_point_updata(11,data_point)
time1 = time.time()

print(time1-time0)

#time.sleep(0.1)
dev.trigger_ctrl(trigger_source,trigger_us,trigger_times,trigger_continue)

test_times+=1
print('test_times',test_times)
#%%

sampling = 0
trigger_source = 0
trigger_us = 500
trigger_times = 1
trigger_continue = 0
###############################system sampling confige#########################
time_start = time.time()
chennel_num = 0


dev.trigger_close()
dev.system_sampling(sampling=sampling,step=0,self_set=1)
for i in range(len(dev.da_ch)):
    dev.dac_Nyquist_cfg(chennel_num=i,Nyquist=0)

#generate data

dac_data = []

if sampling == 0:
    sampleRate=5e9
elif sampling == 1:
    sampleRate=4e9

fstart = 53e6
fnum = 2.5e9/100e6


for i in range(int(fnum)):
    
    fin = fstart+i*100e6
    
    dac_data = []
    datanum = int(fin/1e6*(sampleRate*1e-6))
    
    sin1=WD.Sin(fin*2*np.pi,0,200e-5,sampleRate)*(2**15-1)
    dac_data.append(np.int16(sin1.data)[:datanum])
    
    
    #generate point
    replay_num = 0
    trigger_delay = 0
    replay_cnt = 1
    replay_continue_flag = 1
    
    data_point = []
    data_point_i = [0,0,trigger_delay,replay_cnt,replay_continue_flag]
    data_point.append(data_point_i)
    
    
    
    dev.trigger_close()
    time0 = time.time()
    dev.dac_updata(slot,chennel_num,dac_data[0])
    dev.dac_point_updata(slot,chennel_num,data_point)
    
    time1 = time.time()
    
    print(time1-time0)
    
    #time.sleep(0.1)
    dev.trigger_ctrl(trigger_source,trigger_us,trigger_times,trigger_continue)
    
    time.sleep(2)













