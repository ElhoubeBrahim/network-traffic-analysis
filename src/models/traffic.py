from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import INET, TIMESTAMP

Base = declarative_base()


class Traffic(Base):
    __tablename__ = "traffic"

    id = Column(Integer, primary_key=True)
    src_ip = Column(INET)
    dst_ip = Column(INET)
    src_port = Column(Integer)
    dst_port = Column(Integer)
    protocol = Column(String)
    bytes = Column(Integer)
    type = Column(String)
    timestamp = Column(TIMESTAMP)
