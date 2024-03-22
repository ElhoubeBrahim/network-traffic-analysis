from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import INET, TIMESTAMP

Base = declarative_base()


class Host(Base):
    __tablename__ = "hosts"

    id = Column(Integer, primary_key=True)
    ip = Column(INET)
    first_seen = Column(TIMESTAMP)
    last_seen = Column(TIMESTAMP)
    packets_sent = Column(Integer)
    packets_received = Column(Integer)
    bytes_sent = Column(Integer)
    bytes_received = Column(Integer)
