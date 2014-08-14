import glob
from processdata import processdata
files = glob.glob('kplr004852528/*.fits')
print files
print processdata(files)
