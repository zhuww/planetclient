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

NOP = 1

DBPATH='/home/zhuww/data/Kepler/archive/'
engine = create_engine('sqlite:///%s/kic.db' % DBPATH, echo=True)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


koitab = np.array(np.genfromtxt(DBPATH+'planetserver/cumulative.tab', delimiter='\t')[...,1], dtype=int)

for kic in koitab[:NOP]:
    filelist = [DBPATH + '/data3/keplerpub/' + '/'.join([f.path, f.filename]) for f in session.query(file_table).filter(file_table.kic == int(kic) and file_table.cadence=='llc')]
    print filelist
    print processdata(filelist)

