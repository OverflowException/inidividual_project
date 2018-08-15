import numpy as np
import math

def fft_scaled(sig, fs):
    freq = np.linspace(0, fs, len(sig) + 1)
    freq = freq[0 : len(sig) / 2 + 1]

    spect = np.fft.fft(sig)[0 : len(freq)] / len(sig)
    energy = np.real(spect * np.conj(spect))
    mag = np.sqrt(energy)
    phase = np.angle(spect, deg = True)
    return mag, phase, energy, freq

def get_extrema(sig):
    diff = np.diff(sig)
    #print(diff)
    peak = []
    valley = []
    for i in range(1, len(diff)):
        if diff[i - 1] > 0 and diff[i] < 0:
            peak.append(i)
        if diff[i - 1] < 0 and diff[i] > 0:
            valley.append(i)
    return peak, valley

def profile_points(freq, duration, tstep):
    ncycle = math.ceil(freq * duration)
    npoint = int(math.ceil(ncycle / float(freq) / tstep))
    return npoint

def phshift(sig1, sig2):
    """Calculate phase shift between sine wave signal. Parameters pass by reference."""
    
    #Trim longer signal
    if len(sig2) == len(sig1):
        pass
    elif len(sig2) < len(sig1):
        sig1 = sig1[:len(sig2)]
    else:
        sig2 = sig2[:len(sig1)]

    sig_len = len(sig1)
        
    #eliminate dc component
    dc1 = dc(sig1)
    dc2 = dc(sig2)
    for idx in range(0, sig_len):
        sig1[idx] -= dc1
        sig2[idx] -= dc2

    #Equalize amplitude
    amp1 = (max(sig1) - min(sig1)) / 2
    amp2 = (max(sig2) - min(sig2)) / 2
    #Choose a larger amplitude as scale, better accuracy
    if amp1 > amp2:
        scale = amp1 / amp2
        sig2[:] = [ele * scale for ele in sig2]
    elif amp1 < amp2:
        scale = amp2 / amp1
        sig1[:] = [ele * scale for ele in sig1]

    #Calculate phase shift, in radian
    dot_product = np.dot(sig1, sig2)
    norm_product = np.linalg.norm(sig1) * np.linalg.norm(sig2)
    phshift = math.acos(dot_product / norm_product)

    #Return phase shift and normalized signals
    return phshift, sig1, sig2

def ratio_split(total, ratio):
    result = []
    for i in range(len(ratio)):
        result.append(float(ratio[i]) / sum(ratio[i:]) * total)
        result[-1] = int(round(result[-1]))
        total -= result[-1]
    return result
    
def dc(sig):
    """Get DC component of a signal"""
    return sum(sig) / len(sig)
