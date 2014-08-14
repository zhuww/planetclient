import cPickle
import sklearn.preprocessing as PPC
import sklearn.cross_validation as CV
from sklearn.svm import SVC
import numpy as np
from pylab import *
from ubc_AI.data import cross_validation
from pylab import *

clf = SVC( probability=True)
pos = cPickle.load(open('positive.pkl', 'rb'))
neg = cPickle.load(open('negtive.pkl', 'rb'))
#print len(pos), len(neg)
#sys.exit(0)
posdata = PPC.scale([pos[k] for k in pos], axis=1)
postarget = np.ones(posdata.shape[0])
negdata = PPC.scale([neg[k] for k in neg], axis=1)
negtarget = np.zeros(negdata.shape[0])

#imshow(negdata)
#plot(posdata[1])
#show()
#sys.exit(0)

#print [np.mean(p) for p in posdata]
#print [np.mean(p) for p in negdata]
#print len(postarget), len(negtarget)
#sys.exit(0)


data = np.vstack((posdata,negdata))
target = np.hstack((postarget, negtarget))
#print data.shape
#print target.shape

index = range(len(data))
np.random.shuffle(index)
data = data[index]
target = target[index]
#print target
#sys.exit(0)

datasize = len(data)
#print datasize
#cvs =  CV.cross_val_score(clf, data, target, cv=15, n_jobs=15)
#print "F1: %0.2f (+/- %0.2f)" % (np.mean(cvs),np.std(cvs))
#print cross_validation(clf, data, target, verbose=True)
clf.fit(data, target)
cPickle.dump(clf, open('clfsvm.pkl', 'wb'), protocol=2)

