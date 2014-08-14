import numpy as np
from datatools.fitstools import *


def readfs(files):

    xin = np.array([])
    yin = np.array([])
    ein = np.array([])
    din = np.array([])
    for f in files[:]:
        #print f
        datafile = fitsfile(f)
        BJDREFI = datafile.hdread(key='BJDREFI')
        colnames = datafile.colinfo().names
        #print colnames

        datatable = np.array([a for a in datafile.gettable(cols = ['TIME', 'PDCSAP_FLUX', 'PDCSAP_FLUX_ERR', 'SAP_BKG'])])
        #print datatable

        x = datatable[...,0] + BJDREFI - 2400000
        y = datatable[...,1] 
        yerr = datatable[...,2]

        yerr = yerr[y > 0]
        x = x[y > 0 ]
        y = y[y > 0 ]
        y = y - (y[-1] - y[0])/(x[-1] - x[0]) * (x-x[0]) - y[0]
        y = y - np.median(y)
        d = np.diff(x)


        xin = np.append(xin, x) 
        yin = np.append(yin, y)
        ein = np.append(ein, yerr)
        din = np.append(din, d)


    d = din
    idx = np.argsort(xin)
    x = xin[idx]
    y = yin[idx]
    yerr = ein[idx]
    #print [y[i] for i,t in enumerate(x) if not t>0]
    x = x - np.min(x)


    #print np.median(d), d.max(), d.min(), np.mean(d), np.std(d)
    md = d.min()
    d = d[d<1.5*md]
    dm = np.median(d)
    #print 'average time step', dm
    idx = x/dm
    rem = np.mod(idx, 1)
    for i,dx in enumerate(idx):
        if rem[i] >= 0.5:
            idx[i] = int(idx[i]) + 1
        elif rem[i] < 0.5:
            idx[i] = int(idx[i])
        else:
            #print rem[i]
            raise idx[i]

    #stich padding
    didx = np.diff(idx)
    #print didx.min(), didx.max(), didx.argmax()
    ylength  = len(y)
    i = 1
    j = 1
    ix = np.zeros(idx.max()+1)
    iy = np.zeros(idx.max()+1)
    ie = np.zeros(idx.max()+1)
    ix[0] = x[0]
    iy[0] = y[0]
    for d in didx:
        yv = y[j]
        if not j >= ylength-10:
            if d > 10:
                ynext = np.mean(y[j+1:j+10])
            else:
                ynext = y[j+1]
        else:
            ynext = y[j]
        #if d > 10:
            #print i, iy[i-5:i-1], yv, y[j+1:j+10]
        ev = yerr[j]
        j+=1
        for k in range(int(d)):
            if d > 10:
                iy[i] = np.mean(y[j-5:j-1]) + (ynext-np.mean(y[j-5:j-1]))*k/d
            else:
                iy[i] = yv + (ynext-yv)*k/d
            ie[i] = ev
            ix[i] = i*dm
            i+=1

    return ix, iy, ie
