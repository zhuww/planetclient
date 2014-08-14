import numpy as np

fi = np.loadtxt('finterest.lst', dtype=[('kic', int), ('score', float)])

good = fi[fi['score']>=0.9]
np.savetxt('goodlist_7prc.txt', good, fmt='%s')
