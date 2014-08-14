from numpy.fft import *
import numpy as np

#def fftsmooth(y, cutfreq=0.004):
def fftsmooth(y, cutfreq=0.01):
    freq = fftfreq(len(y))
    trans = rfft(y)
    #print 'freq:', freq[:trans.size-1], freq[0], freq[trans.size-2],trans.size-1
    #print 'freq cut:',cutfreq/freq[trans.size-2]*(trans.size-1)
    ncut = int(cutfreq/freq[trans.size-2]*(trans.size-1))
    newtrans = np.array([0+0j for i,t in enumerate(trans) if i <= ncut] + [t for i,t in enumerate(trans) if i>ncut])
    smoothedy = irfft(newtrans)
    return smoothedy

from  scipy.signal import lfilter#, medfilt
from scipy.signal import filter_design

#b,a = filter_design.butter(1, 0.03, btype='high', ouput='ba')
b,a = filter_design.ellip(1, 1., 1., 0.03, btype='high', output='ba')
def filtersmooth(y):
    #return medfilt(y, kernel_size=251)
    return lfilter(b,a,y)
