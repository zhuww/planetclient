import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Integer, String

class file_table(Base):
    __tablename__ = "Files"

    filename = Column( String(36), primary_key=True),
    dir = Column(String(10)),
    kic = Column(Integer),
    cadence = Column(String(3))

    def __init__(self, filename, dir, kic, cadence):
        self.filename = filename
        self.dir = dir
        self.kic = kic
        self.cadence

    def __repr__(self):
        return "<File('%s/%s')>" % (self.dir, self.filename)

