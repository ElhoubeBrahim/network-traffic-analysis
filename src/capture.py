from scapy.all import sniff
from kafka import KafkaProducer
import json
from utils import get_application_protocol

producer = KafkaProducer(
    bootstrap_servers=["localhost:29092"],
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)


# Process captured packets
def process_packet(packet):
    # Skip IPv6 packets
    if packet[0][1].name != "IP":
        return

    # Extract packet relevant information
    packet = {
        "ip": {
            "src": packet[0][1].src,
            "dst": packet[0][1].dst,
        },
        "protocol": get_application_protocol(packet),
        "size": packet[0][1].len,  # Bytes
        "port": {
            "src": packet[0][1].sport,
            "dst": packet[0][1].dport,
        },
        "type": packet.name,
        "timestamp": packet.time,
    }

    # Send packet to Kafka
    producer.send("packets", packet)
    producer.flush()


# Capture network packets
sniff(prn=process_packet)
