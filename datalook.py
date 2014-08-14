from datatools.fitstools import *
from pylab import *
import sys, os
import numpy as np
import glob
from numpy.fft import *
#from scipy.signal import find_peaks_cwt

files = glob.glob('kplr004852528/*.fits')


ax1 = subplot(311)
ax2 = subplot(312)
ax3 = subplot(313)
for f in files[:]:
    datafile = fitsfile(f)
    BJDREFI = datafile.hdread(key='BJDREFI')
    colnames = datafile.colinfo().names
    #print colnames

    datatable = np.array([a for a in datafile.gettable(cols = ['TIME', 'PDCSAP_FLUX', 'PDCSAP_FLUX_ERR', 'SAP_BKG']) if a[1]>0])
    #print datatable

    x = datatable[...,0] + BJDREFI - 2400000
    y = datatable[...,1] 
    y = y - y[0]
    y = y - (y[-1] - y[0])/(x[-1] - x[0]) * (x-x[0])

    #y = datatable[...,1] 
    #xy = np.vstack((x, y)).T
    #print cspline2d(xy, 0.5)
    yerr = datatable[...,2]
    trans = rfft(y)
    etrans = rfft(yerr)
    newtrans = np.array([0+0j for i,t in enumerate(trans) if i <= 30] + [t for i,t in enumerate(trans) if i>30])
    smoothedy = irfft(newtrans)
    #print x.shape, y.shape, smoothedy.shape
    ax1.errorbar(x, y, yerr=yerr, color='b', alpha=0.5)
    ax2.plot(x[:len(smoothedy)], smoothedy, color='r')
    ax3.plot(x[:len(smoothedy)], smoothedy, color='r')

    #peakind = find_peaks_cwt(smoothedy, np.arange(2.0,2.5, 0.5), min_snr=3.)
    #print np.arange(2.0,2.5, 0.5)
    #print len(peakind)
    #for peak in peakind:
        #ax3.axvline(x = x[peak], color='g', alpha=0.5)
xlabel('MJD')
ylabel('Flux')
show()
