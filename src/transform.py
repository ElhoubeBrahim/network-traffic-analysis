from kafka import KafkaConsumer
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from datetime import datetime
import json
from utils import get_geoip_info

from models.traffic import Traffic
from models.geoip import GeoIP

# Connect to Kafka
consumer = KafkaConsumer(
    "packets",
    bootstrap_servers=["localhost:29092"],
    value_deserializer=lambda v: json.loads(v),
)

# Connect to database
engine = create_engine("postgresql://postgres:postgres@localhost:5432/packets")

# For each packet in Kafka
with Session(engine) as connection:
    for message in consumer:
        # Get packet from Kafka
        packet = message.value

        # Save packet to database
        traffic = Traffic(
            src_ip=packet["ip"]["src"],
            dst_ip=packet["ip"]["dst"],
            src_port=packet["port"]["src"],
            dst_port=packet["port"]["dst"],
            protocol=packet["protocol"],
            bytes=packet["size"],
            type=packet["type"],
            timestamp=datetime.fromtimestamp(packet["timestamp"]),
        )
        connection.add(traffic)

        # Get GeoIP information
        src_geoip = get_geoip_info(packet["ip"]["src"])
        dst_geoip = get_geoip_info(packet["ip"]["dst"])

        # Save src GeoIP information to database
        if src_geoip is not None:
            stmt = insert(GeoIP).values(
                ip=packet["ip"]["src"],
                country_code=src_geoip["country"]["code"],
                country_name=src_geoip["country"]["name"],
                city=src_geoip["city"],
                latitude=src_geoip["latitude"],
                longitude=src_geoip["longitude"],
            )
            stmt = stmt.on_conflict_do_update(
                index_elements=["ip"],
                set_={
                    "country_code": stmt.excluded.country_code,
                    "country_name": stmt.excluded.country_name,
                    "city": stmt.excluded.city,
                    "latitude": stmt.excluded.latitude,
                    "longitude": stmt.excluded.longitude,
                },
            )
            connection.execute(stmt)

        # Save dst GeoIP information to database
        if dst_geoip is not None:
            stmt = insert(GeoIP).values(
                ip=packet["ip"]["dst"],
                country_code=dst_geoip["country"]["code"],
                country_name=dst_geoip["country"]["name"],
                city=dst_geoip["city"],
                latitude=dst_geoip["latitude"],
                longitude=dst_geoip["longitude"],
            )
            stmt = stmt.on_conflict_do_update(
                index_elements=["ip"],
                set_={
                    "country_code": stmt.excluded.country_code,
                    "country_name": stmt.excluded.country_name,
                    "city": stmt.excluded.city,
                    "latitude": stmt.excluded.latitude,
                    "longitude": stmt.excluded.longitude,
                },
            )
            connection.execute(stmt)

        # Commit transaction
        connection.commit()
