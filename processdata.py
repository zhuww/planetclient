from numpy.fft import *
from smooth import fftsmooth, filtersmooth
from fold import fold
from blssearch import bls
from readfiles import readfs
import numpy as np

from pylab import *
ax1 = subplot(411)
ax2 = subplot(412)
ax3 = subplot(413)
ax4 = subplot(414)

def processdata(files):
    ix,iy,ie = readfs(files)

    ax1.errorbar(ix, iy, yerr=ie, color='b', alpha=0.5)

    smoothedy = fftsmooth(iy)

    ax2.plot(ix[:len(smoothedy)], smoothedy, color='r')

    ix = ix[:len(smoothedy)]
    T = ix.max() - ix.min()
    nf = min(10000, ix.size * 2)
    minperiod, maxperiod = 0.5, T-1 #min([100., T-1])
    fmin, df = 1./maxperiod, (1./minperiod - 1./maxperiod)/nf
    freqs = np.arange(fmin, fmin+df*nf, df)[:nf]
    p, bper, bpow, depth, qtran, in1, in2 = bls(ix, smoothedy, nf=nf, fmin=fmin, df=df)

    a = 1./freqs
    b = p 
    coeff = np.polyfit(a,b,3)
    polys = np.poly1d(coeff)
    ys = polys(a)

    ax3.plot(a, np.exp(p-ys))
    #ax3.plot(a, ys, 'r-')
    ax3.set_xscale('log')
    ax3.set_xlim([minperiod, maxperiod])
    ax3.axvline(x=bper, color='r', linewidth=1)

    nbin = 100
    binvalue,binerr = fold(ix, smoothedy, bper, yerr=ie, bins=nbin)
    ax4.step(np.arange(0,1,1./nbin)+0.5/nbin, binvalue, color='b')
    foldedcurve = ax4.errorbar(np.arange(0,1,1./nbin), binvalue, yerr=binerr, fmt='.', color='b')

    show()
    return binvalue
