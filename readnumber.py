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

#import sklearn.preprocessing as PPC
def normalize(arr):
    mean = np.mean(arr)
    arr -= mean
    std = np.std(arr)
    arr /= std
    return arr

class scan(object):
    def __enter__(self):
        self.cwd = os.getcwd()
        self.result = {}
        try:
            self.processed = cPickle.load(open('processed.pkl', 'rb'))
        except:
            self.processed = np.array([])
        return (self.result,self.processed)
    def __exit__(self, exc_type, exc_value, exc_tb):
        os.chdir(self.cwd)
        try:
            result = cPickle.load(open('quicklc_all.pkl', 'r'))
            result.update(self.result)
            processed = cPickle.load(open('processed.pkl', 'r'))
            processed = np.append(processed, self.processed)
        except:
            result = self.result
            processed = self.processed
        cPickle.dump(processed, open('processed.pkl', 'w'),protocol=2)
        cPickle.dump(result, open('quicklc_all.pkl', 'w'),protocol=2)

        if exc_type is KeyboardInterrupt:
            print '\nManually Stopped\n'
            return True
        else:
            return exc_type is None
        print '\nFinish running\n' 


batchsize = 10

#DBPATH='/home/zhuww/data/Kepler/archive/'
#engine = create_engine('sqlite:///%s/kic.db' % DBPATH, echo=False)
#Session = sessionmaker()
#Session.configure(bind=engine)
#session = Session()


#koitab = np.array(np.genfromtxt(DBPATH+'planetserver/cumulative.tab', delimiter='\t')[...,1], dtype=int)
#koitab = np.array(np.genfromtxt(DBPATH+'planetserver/tce.tab', delimiter='\t')[...,1], dtype=int)
#allkics = np.array(list(set(np.load(DBPATH+"planetserver/allkic.npz")['allkics'])))
EB = set(np.genfromtxt('./EB.tab', dtype=int))
FP = set(np.genfromtxt('./FP.tab', dtype=int))

print 'EB, FP: ', len(EB), len(FP)

sys.exit(0)
goodkics = np.array(list(set(koitab)))

#randidx = np.random.randint(0, allkics.size, len(kiclist))
randidx = np.random.randint(0, allkics.size, len(allkics))
kiclist = allkics[randidx]



clf = cPickle.load(open('clfsvm.pkl', 'rb'))

fint = open('finterest.lst', 'w')

def batchjob(kic):
    try:
        filelist = [DBPATH + '/data3/keplerpub/' + '/'.join([f.path, f.filename]) for f in session.query(file_table).filter(file_table.kic == int(kic) and file_table.cadence=='llc') if f.filename.endswith('llc.fits')]
        lc, period, depth,Ttran, epoch = processdata(filelist)
        p = clf.predict_proba(normalize(lc))
    #print p
        if p[0][1] > 0.9 and depth<0.01 and period > 1. and not kic in set(goodkics):
            fint.write('%s %s %s %s %s\n' % (kic, period, depth, Ttran, epoch))
            fint.flush()
            return {kic: (lc, period, depth,Ttran, epoch)}
        else:
            return {}
    except:
        return {}

with scan() as data:
    result, processed = data
    kiclist = np.array(list(set(kiclist) - set(processed) - set(koitab) - EB - FP))
    batchnumber = len(kiclist)/batchsize
    batchs = np.array_split(kiclist, batchnumber)
    N_batchs = len(batchs)
    print 'N_batchs:', N_batchs
    pb = PB(maxValue=N_batchs)
    for i,batch in enumerate(batchs):
        batchres = threadit.threadit(batchjob, [[b] for b in batch])
        for b in batchres:
            result.update(b)
        pb(i)
        processed = np.append(processed, batchs)


    fint.close()
    #cPickle.dump(result, open('quicklc_all.pkl', 'wb'), protocol=2)
#cPickle.dump(result, open('negtive.pkl', 'wb'), protocol=2)
#result = np.array(result)
#print len(result)
#np.savez('scanresult.npz', **result)
