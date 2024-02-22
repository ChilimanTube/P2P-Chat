from network import UDPDiscovery, TCPConnector, MessageHandler
import threading

if __name__ == "__main__":
    peer_id = "renegade"  # TODO: make ID configurable in a config file
    UDPDiscovery.broadcast_and_listen(peer_id)
    print("Starting TCP server...")
    threading.Thread(target=TCPConnector.start_server, args=('localhost', 9876, MessageHandler.get_messages_history()), daemon=True).start()
    print("TCP server started.")