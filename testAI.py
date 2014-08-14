import cPickle
import sklearn.preprocessing as PPC
import sklearn.cross_validation as CV
from sklearn.svm import SVC
import numpy as np

clf = SVC()
pos = cPickle.load(open('positive.pkl', 'rb'))
neg = cPickle.load(open('negtive.pkl', 'rb'))
posdata = PPC.scale([pos[k] for k in pos])
postarget = np.ones(posdata.size)
negdata = PPC.scale([neg[k] for k in neg])
negtarget = np.zeros(negdata.size)

data = np.concatenate(posdata,negdata)
target = np.concatenate(postarget, negtarget)

index = range(len(data))
np.random.shuffle(index)
data = data[index]
target = target[index]

datasize = len(data)
print datasize
print CV.cross_val_score(clf, data, target)
