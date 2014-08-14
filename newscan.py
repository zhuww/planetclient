from defdb import file_table
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from ProgressBar import progressBar as PB

from processdata import processdata

from smooth import fftsmooth, filtersmooth
from fold import fold
from blssearch import bls
from readfiles import readfs

import threadit
import cPickle

def normalize(arr):
    mean = np.mean(arr)
    arr -= mean
    std = np.std(arr)
    arr /= std
    return arr

NOP = -1
batchsize = 10

DBPATH='/home/zhuww/data/Kepler/archive/'
engine = create_engine('sqlite:///%s/kic.db' % DBPATH, echo=False)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


koitab = np.array(np.genfromtxt(DBPATH+'planetserver/cumulative.tab', delimiter='\t')[...,1], dtype=int)
#allkics = np.load(DBPATH+"planetserver/allkic.npz")['allkics']

kictab = np.loadtxt('finterest.lst', dtype=[('kic', int), ('score', float)])
allkics = kictab[kictab['score']>=0.9]['kic']
print allkics
print len(allkics)


goodkics = np.array(list(set(koitab[:NOP])))

#randidx = np.random.randint(0, allkics.size, len(kiclist))
randidx = np.random.randint(0, allkics.size, len(allkics))
kiclist = allkics[randidx]

batchnumber = len(kiclist)/batchsize
batchs = np.array_split(kiclist, batchnumber)
N_batchs = len(batchs)

print 'N_batchs:', N_batchs

pb = PB(maxValue=N_batchs)

clf = cPickle.load(open('clfsvm.pkl', 'rb'))

fint = open('moreresult.lst', 'w')

def batchjob(kic):
    filelist = [DBPATH + '/data3/keplerpub/' + '/'.join([f.path, f.filename]) for f in session.query(file_table).filter(file_table.kic == int(kic) and file_table.cadence=='llc') if f.filename.endswith('llc.fits')]
    lc, period, depth,Ttran, epoch = processdata(filelist)
    p = clf.predict_proba(normalize(lc))
    #print p
    if p[0][1] > 0.5 and not kic in set(goodkics):
        fint.write('%s %s %s %s %s\n' % (kic, period, depth, Ttran, epoch))
        fint.flush()
    return {kic: lc}

result = {}
for i,batch in enumerate(batchs):
    batchres = threadit.threadit(batchjob, [[b] for b in batch])
    for b in batchres:
        result.update(b)
    pb(i)

fint.close()
cPickle.dump(result, open('quicklc_7pct.pkl', 'wb'), protocol=2)
#cPickle.dump(result, open('negtive.pkl', 'wb'), protocol=2)
#result = np.array(result)
#print len(result)
#np.savez('scanresult.npz', **result)
