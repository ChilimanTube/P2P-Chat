from network import UDPDiscovery
from config import config

if __name__ == "__main__":
    peer_id = "renegade"  # TODO: make ID configurable in a config file
    UDPDiscovery.broadcast_and_listen(peer_id)
