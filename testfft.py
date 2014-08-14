from numpy.fft import *
import numpy as np
import glob
from readfiles import readfs
from pylab import *
from smooth import *
from scipy import mgrid
from fold import fold
#from intplot import AnnoteFinder
from cursorinteraction import Cursor 
import copy


files = glob.glob('kplr007109675/*.fits')
#files = glob.glob('kplr004852528/*.fits')
#files = glob.glob('./*.fits')
ix,iy,ie = readfs(files)
#iy = fftsmooth(iy)

freq = fftfreq(len(iy), 0.0204336469852)
trans = np.abs(rfft(iy))
etrans = np.abs(rfft(ie))

harmsum = np.zeros(len(trans))
for i in [2,4,8,16,32]:
    halftrans = trans[:len(trans)/i]
    coords = mgrid[0:freq[len(trans)/i]:1j*len(trans)/i]
    #print len(halftrans),len(trans)/i, coords
    newcoords = mgrid[0:freq[len(trans)-1]:1j*len(trans)]
    harmsum += np.interp(newcoords, coords, halftrans)
trans += harmsum

#sys.exit(0)
#print len(trans)
#print len(freq)
#print freq

ax1 = subplot(311)
ax2 = subplot(312)
ax3 = subplot(313)
ax1.errorbar(ix, iy, yerr=ie, color='b', alpha=0.5)
#ax2.errorbar(1./freq[1:len(trans)-1], trans[1:-1], yerr=etrans[1:-1])
ax2.plot(1./freq[1:len(trans)-1], trans[1:-1])
xdata = copy.deepcopy(1./freq[1:len(trans)-1])
ydata = copy.deepcopy(trans[1:-1])
cursor = Cursor(ax2, xdata, ydata)
connect('motion_notify_event', cursor.mouse_move)
connect('button_press_event', cursor.click)

peak = np.argmax(trans[1:len(trans)-1])
period = xdata[peak]
print peak, period
nbin = 300
binvalue,binerr = fold(ix, iy, period, yerr=ie, bins=nbin)
ax3.step(np.arange(0,1,1./nbin)+0.5/nbin, binvalue, color='b')
ax3.errorbar(np.arange(0,1,1./nbin), binvalue, yerr=binerr, fmt='.', color='b')

def folding():
    ax3.cla()
    print cursor.end,cursor.start, len(ydata), ydata[cursor.end:cursor.start]
    peak = cursor.end + np.argmax(ydata[cursor.end:cursor.start])
    period = xdata[peak]
    print peak, period
    binvalue,binerr = fold(ix, iy, period, yerr=ie, bins=nbin)
    ax3.step(np.arange(0,1,1./nbin)+0.5/nbin, binvalue, color='b')
    ax3.errorbar(np.arange(0,1,1./nbin), binvalue, yerr=binerr, fmt='.', color='b')

cursor.link_exe(folding)


gca().set_autoscale_on(False)
show()
