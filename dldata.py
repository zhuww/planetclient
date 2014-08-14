import urllib
from ftplib import FTP
import os,sys


def  download(kic, path='./'):
    kic = kic.rjust(9, '0')
    print "downloading %s. This could take few minutes." % kic
    try:
        url = 'http://archive.stsci.edu/pub/kepler/lightcurves/' + kic[:4] + '/' + kic + '/' 
        print url
        os.system("wget -q -nH --cut-dirs=6 -r -l0 -c -N -np -R 'index*' -erobots=off  --directory-prefix=%s -A.fits %s " % (path+"/kplr"+kic, url))
        #filename = wget.download(url, wget.progress_callback)
        #print filename
        #filename='newfile.fits'
        return True
    except Exception, e:
        print 'Exception: ', e
        return False

if __name__ == "__main__":
    kic = sys.argv[1]
    print kic
    download(kic)

