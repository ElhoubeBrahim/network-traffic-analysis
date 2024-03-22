import geoip2.database

def get_application_protocol(packet):
    layers = []

    # Start with the first layer of the packet
    current_layer = packet
    while current_layer.payload:
        current_layer = current_layer.payload
        layers.append(current_layer.name)

    # Return the name of the last layer if it's not raw
    return layers[-1] if layers[-1] != "Raw" else layers[-2]


def get_geoip_info(ip):
    with geoip2.database.Reader("geolite2.mmdb") as reader:
        try:
            response = reader.city(ip)

            return {
                "country": {
                    "code": response.country.iso_code,
                    "name": response.country.name,
                },
                "city": response.city.name,
                "latitude": response.location.latitude,
                "longitude": response.location.longitude,
            }
        except geoip2.errors.AddressNotFoundError:
            return None
