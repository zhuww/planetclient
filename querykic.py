from defdb import file_table
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from ProgressBar import progressBar as PB

NOP = 10

DBPATH='/home/zhuww/data/Kepler/archive/'
engine = create_engine('sqlite:///%s/kic.db' % DBPATH, echo=True)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

#allkics = np.load("allkic.npz")["allkics"]
koitab = np.array(np.genfromtxt(DBPATH+'planetserver/cumulative.tab', delimiter='\t')[...,1], dtype=int)
#filelist = []
#for koi in koitab[0:10]:
filelist = [r'/'.join([f.path, f.filename]) for f in session.query(file_table).filter(file_table.kic.in_([int(i) for i in koitab[0:NOP]])  ).filter(file_table.cadence=='llc')]
#print filelist
answers = []
pb = PB(len(filelist))
for i,fp in enumerate(filelist):
    pb(i)
    answers.append(os.access(DBPATH + '/data3/keplerpub/' + fp, os.R_OK))

print len(answers)
print all(answers)
