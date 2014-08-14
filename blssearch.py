import BLS
import numpy as np


def bls(ix, y, nb=500, qmi=1.e-3, qma=0.2, nf=8000, fmin=0.01, df=5.e-5):
    n = len(y)
    u = np.zeros(n)
    v = np.zeros(n)
    #nf,fmin,df = 8000, 0.01, 5.e-5
    #nf,fmin,df = 1000, fmin, df
    #print nf, 1./fmin, 1./(fmin+nf*df)
    #print n, ix.size, y.size
    p = np.zeros(nf)
    pout = np.zeros(6)
    BLS.fbls(n,ix,y,u,v,nf,fmin,df,nb,qmi,qma, p, pout)
    bper, bpow, depth, qtran, in1, in2 = pout
    return p, bper, bpow, depth, qtran, in1, in2
