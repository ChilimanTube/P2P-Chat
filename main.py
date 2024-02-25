from network import UDPDiscovery
import json

if __name__ == "__main__":
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
        UDPDiscovery.broadcast_and_listen(config["peer_id"])
