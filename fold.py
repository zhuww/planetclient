import numpy as np

def fold(x, y, period, yerr=None, bins=30, peak={}):
    phase = np.mod(x, period)/period
    pbins = np.linspace(0,1, bins+1)
    binvalue = np.zeros(bins)
    if not yerr == None:binerr = np.zeros(bins)
    idx = np.argsort(phase)
    phase = phase[idx]
    y = y[idx]
    j = 0
    for i,p in enumerate(phase):
        if p < pbins[j+1]:
            binvalue[j] += y[i]
            if not yerr == None:binerr[j]+=yerr[i]**2
        else:
            j+=1
            binvalue[j] += y[i]
            if not yerr == None:binerr[j]+=yerr[i]**2
    align = binvalue.argmin()
    peak['offset'] = align/bins
    binvalue = np.roll(binvalue, bins/2-align)
    if not yerr == None:binerr = np.sqrt(np.roll(binerr, bins/2-align))
    if not yerr == None:return binvalue, binerr
    return binvalue
