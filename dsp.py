import numpy as np
from scipy import fftpack


def fft_filter(signal,time,type,offset=False,*argv):
  
    #Signal : A numpy array float or int
    #Time   : A numpy array float or int
    #Type   : A string that defines the filter type
    #         'bpf' = Band Pass Filter
    #         'lbf' = Low Pass filter
    #         'hpf' = High Pass filter
    #         'rpf' = Reject Band filter
    #Offset : default is False. If True, it will return the signal with offset (signal filterde + mean of the original signal)
    #*argv  : Cutoff frequencies. The fist argument must be the low frequency and the second the high frequency for hpf and rpf
    #         For lpf or hpf it will just need one argument that will be the cutoff frequency.
    cutoff=[]
    for arg in argv:
        cutoff.append(arg)
    
    #get the time step to define sample rate
    time_step = time[1]-time[0]
    
    #Apply de FFT to the signal
    sig_fft = fftpack.fft(signal)    
    
    #Define the spectrum
    sample_freq = fftpack.fftfreq(signal.size, d=time_step)
    
    if(type == 'bpf'):
        
        band_pass_fft = sig_fft.copy()
        band_pass_fft[np.abs(sample_freq)<cutoff[0]]=0
        band_pass_fft[np.abs(sample_freq)>cutoff[1]]=0
        filtered_sig = fftpack.ifft(band_pass_fft)
        
    elif(type == 'lpf'):
        low_pass_fft = sig_fft.copy()
        low_pass_fft[np.abs(sample_freq)>cutoff[0]]=0
        filtered_sig = fftpack.ifft(low_pass_fft)
        
    elif(type == 'hpf'):
        high_pass_fft = sig_fft.copy()
        high_pass_fft[np.abs(sample_freq)<cutoff[0]]=0
        filtered_sig = fftpack.ifft(high_pass_fft)
    
    elif(type == 'rbf'):
        reject_band_fft = sig_fft.copy()
        reject_band_fft[np.abs(sample_freq)>cutoff[0]]=0
        reject_band_fft[np.abs(sample_freq)<cutoff[1]]=0
        filtered_sig = fftpack.ifft(reject_band_fft)
    
    if (offset==False):
        return filtered_sig
    else:
        media_sinal=signal.mean()
        return filtered_sig+media_sinal