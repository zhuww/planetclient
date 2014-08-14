from sqlalchemy import MetaData, Column, Table, ForeignKey
from sqlalchemy import Integer, String

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class file_table(Base):
    __tablename__ = "file_table"

    filename = Column(String(36), primary_key=True)
    path = Column(String(10))
    kic = Column(Integer)
    cadence = Column(String(3))
    def __init__(self, filename, path, kic, cadence):
        self.filename = filename
        self.path = path
        self.kic = kic
        self.cadence = cadence
    def __repr__(self):
        return "<%s/%s>" % (self.path, self.filename)
#print file_table.__table__
