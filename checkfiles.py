import glob,sys
import numpy as np
from smooth import fftsmooth, filtersmooth
from fold import fold
from blssearch import bls
from readfiles import readfs
from processdata import processdata

from defdb import file_table
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from foldnplot import main

DBPATH='/home/zhuww/data/Kepler/archive/'
engine = create_engine('sqlite:///%s/kic.db' % DBPATH, echo=False)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

kic = sys.argv[1]
kic = kic.rjust(9, '0')
files = glob.glob('./data/kplr'+kic+'/*llc.fits')

#ix,iy,ie,x0,ym = readfs(files)
#lc, period, depth,Ttran, epoch = processdata(files)
#print kic, period, depth, Ttran, epoch


filelist = [DBPATH + '/data3/keplerpub/' + '/'.join([f.path, f.filename]) for f in session.query(file_table).filter(file_table.kic == int(kic) and file_table.cadence=='llc') if f.filename.endswith('llc.fits')]
#lc, period, depth,Ttran, epoch = processdata(filelist)
#print kic, period, depth, Ttran, epoch
main(kic, files=filelist)
