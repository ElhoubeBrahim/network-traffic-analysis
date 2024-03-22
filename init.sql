CREATE TABLE traffic (
    id SERIAL PRIMARY KEY,
    src_ip INET,
    dst_ip INET,
    src_port INTEGER,
    dst_port INTEGER,
    protocol VARCHAR(50),
    bytes INTEGER,
    type VARCHAR(50),
    timestamp TIMESTAMP
);

CREATE TABLE hosts (
    id SERIAL PRIMARY KEY,
    ip INET,
    first_seen TIMESTAMP,
    last_seen TIMESTAMP,
    packets_sent INTEGER,
    packets_received INTEGER,
    bytes_sent INTEGER,
    bytes_received INTEGER
);

CREATE TABLE geoip (
    ip INET PRIMARY KEY,
    country_code CHAR(2),
    country_name VARCHAR(50),
    city VARCHAR(50),
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION
);

-- Create a trigger to update the hosts table when a new row is inserted into the traffic table
CREATE OR REPLACE FUNCTION update_hosts() RETURNS TRIGGER AS 

$$

BEGIN

    -- Check if the source IP address is already in the hosts table
    IF EXISTS (SELECT 1 FROM hosts WHERE ip = NEW.src_ip) THEN
        -- Update the existing row
        UPDATE hosts
        SET last_seen = NEW.timestamp,
            packets_sent = packets_sent + 1,
            bytes_sent = bytes_sent + NEW.bytes
        WHERE ip = NEW.src_ip;
    ELSE
        -- Insert a new row
        INSERT INTO hosts (ip, first_seen, last_seen, packets_sent, packets_received, bytes_sent, bytes_received)
        VALUES (NEW.src_ip, NEW.timestamp, NEW.timestamp, 1, 0, NEW.bytes, 0);
    END IF;

    -- Check if the destination IP address is already in the hosts table
    IF EXISTS (SELECT 1 FROM hosts WHERE ip = NEW.dst_ip) THEN
        -- Update the existing row
        UPDATE hosts
        SET last_seen = NEW.timestamp,
            packets_received = packets_received + 1,
            bytes_received = bytes_received + NEW.bytes
        WHERE ip = NEW.dst_ip;
    ELSE
        -- Insert a new row
        INSERT INTO hosts (ip, first_seen, last_seen, packets_sent, packets_received, bytes_sent, bytes_received)
        VALUES (NEW.dst_ip, NEW.timestamp, NEW.timestamp, 0, 1, 0, NEW.bytes);
    END IF;

    RETURN NEW;

END;

$$

LANGUAGE plpgsql;

CREATE TRIGGER update_hosts_trigger
AFTER INSERT ON traffic
FOR EACH ROW
EXECUTE PROCEDURE update_hosts();
