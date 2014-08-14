from pylab import *
import sys, os
import numpy as np
import glob
from numpy.fft import *
from scipy.stats import chi2 
from peakdetect import peakdetect
from smooth import fftsmooth, filtersmooth
from fold import fold
from blssearch import bls
from readfiles import readfs
from cursorinteraction import Cursor 
import copy
from dldata import download


kic = sys.argv[1]
bperiod = float(sys.argv[2])
download(kic, path='./data/')
kic = kic.rjust(9, '0')
files = glob.glob('./data/kplr'+kic+'/*llc.fits')
print files


ix,iy,ie,x0,ym = readfs(files)
ax2 = subplot(111)
#ax2 = subplot(212)


#ax1.errorbar(ix, iy, yerr=ie, color='b', alpha=0.5)

smoothedy = fftsmooth(iy)
#smoothedy = filtersmooth(iy)
ax2.plot(ix[:len(smoothedy)], smoothedy, color='r')
ix = ix[:len(smoothedy)]
        
T = ix.max() - ix.min()
nbin = 1000
binvalue,binerr = fold(ix, iy, bperiod, yerr=ie, bins=nbin)
#ax2.step(np.arange(0,1,1./nbin)+0.5/nbin, binvalue, color='b')
foldedcurve = ax2.errorbar(np.arange(0,1,1./nbin), binvalue, yerr=binerr, fmt='.', color='b')
ax2.set_xlim(0,1)
show()
