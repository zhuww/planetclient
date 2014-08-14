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


#files = glob.glob('kplr007109675/*.fits')
#files = glob.glob('kplr004852528/*.fits')
#files = glob.glob('./data/archive/data3/keplerpub/KOI_public/%s*llc.fits' % sys.argv[1])
kic = sys.argv[1]
download(kic, path='./data/')
kic = kic.rjust(9, '0')
files = glob.glob('./data/kplr'+kic+'/*llc.fits')
print files
#sys.exit(0)
#files = ['./data/archive/data3/keplerpub/KOI_public/'+f for f in sys.argv[1:]]


ax1 = subplot(411)
ax2 = subplot(412)
ax3 = subplot(413)
ax4 = subplot(414)

ix,iy,ie,x0,ym = readfs(files)

ax1.errorbar(ix, iy, yerr=ie, color='b', alpha=0.5)

smoothedy = fftsmooth(iy)
#smoothedy = filtersmooth(iy)
ax2.plot(ix[:len(smoothedy)], smoothedy, color='r')
ix = ix[:len(smoothedy)]
        
#Delta = dm
T = ix.max() - ix.min()
#fc = 1./Delta/2.
#fmin = 20./T
#FD = fc - fmin
#df = FD/1000
#print 'total time span', T

#nf = 10000
nf = min(10000, ix.size * 2)
minperiod, maxperiod = 0.5, T-1 #min([100., T-1])
fmin, df = 1./maxperiod, (1./minperiod - 1./maxperiod)/nf
#nf,fmin,df = 8000, 0.15, 2.e-4
freqs = np.arange(fmin, fmin+df*nf, df)[:nf]
p, bper, bpow, depth, qtran, in1, in2 = bls(ix, smoothedy, nf=nf, fmin=fmin, df=df)
#print bper, bpow, depth, qtran, in1, in2
Ttran = (in1 + in2)/2.0/500.*bper 
print 'candidate period: ', bper, Ttran, in1, in2
ax1.axvline(x=Ttran, color='r', linewidth=1)

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
#print chi2.sf(bpow, 500-1)/nf

xdata = copy.deepcopy(1./freqs)
ydata = copy.deepcopy(p)
cursor = Cursor(ax3, xdata, ydata)
connect('motion_notify_event', cursor.mouse_move)
connect('button_press_event', cursor.click)


nbin = 100
binvalue,binerr = fold(ix, smoothedy, bper, yerr=ie, bins=nbin)
ax4.step(np.arange(0,1,1./nbin)+0.5/nbin, binvalue, color='b')
foldedcurve = ax4.errorbar(np.arange(0,1,1./nbin), binvalue, yerr=binerr, fmt='.', color='b')



def folding():
    ax4.cla()
    #foldedcurve[0].remove()
    #print cursor.end,cursor.start, len(ydata), ydata[cursor.end:cursor.start]
    peak = cursor.end + np.argmax(ydata[cursor.end:cursor.start])
    period = xdata[peak]
    print 'candidate period: ', period
    #binvalue,binerr = fold(ix, iy, period, yerr=ie, bins=nbin)
    binvalue,binerr = fold(ix, smoothedy, period, yerr=ie, bins=nbin)
    ax4.step(np.arange(0,1,1./nbin)+0.5/nbin, binvalue, color='b')
    ax4.errorbar(np.arange(0,1,1./nbin), binvalue, yerr=binerr, fmt='.', color='b')

cursor.link_exe(folding)


ax1.set_xlabel('day')
ax2.set_xlabel('day')
ax3.set_xlabel('day')
ax4.set_xlabel('phase')

show()
