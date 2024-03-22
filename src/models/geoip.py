from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Double
from sqlalchemy.dialects.postgresql import INET

Base = declarative_base()


class GeoIP(Base):
    __tablename__ = "geoip"

    ip = Column(INET, primary_key=True)
    country_code = Column(String)
    country_name = Column(String)
    city = Column(String)
    latitude = Column(Double)
    longitude = Column(Double)
