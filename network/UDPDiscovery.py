import socket
import json
import threading
import time
from network import TCPConnector, MessageHandler


def send_response(sock, addr, peer_id):
    response = json.dumps({"status": "ok", "peer_id": peer_id})
    sock.sendto(response.encode(), addr)
    print(f"UDP: Sent response: {response} to {addr}")


def broadcast_and_listen(peer_id, broadcast_address='172.31.255.255', port=9876):
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', port)) # Bind to listen for responses

    def listen_for_responses():
        while True:
            data, addr = sock.recvfrom(1024)
            try:
                message = json.loads(data.decode())
                if isinstance(message, dict):
                    if message.get("status") == "ok" and message.get("peer_id") != peer_id:
                        print(f"UDP: Received OK from {message['peer_id']} at {addr}")
                        peer_address = addr[0]
                        threading.Thread(target=TCPConnector.send_hello, args=(peer_address, 9876, peer_id)).start()
                    elif message.get("command") == "hello" and message.get("peer_id") != peer_id:
                        send_response(sock, addr, peer_id)
            except json.JSONDecodeError:
                print(f"UDP: Received non-JSON data from {addr}: {data}")
            except Exception as e:
                print(f"UDP: Error handling message from {addr}: {e}")

    def broadcast_message():
        while True:
            print(f"UDP: Broadcasting hello message from {peer_id}")
            message = json.dumps({"command": "hello", "peer_id": peer_id})
            sock.sendto(message.encode(), (broadcast_address, port))
            time.sleep(5)

    # Start listening thread
    threading.Thread(target=listen_for_responses, daemon=True).start()
    # Start broadcasting
    broadcast_message()

    threading.Thread(target=TCPConnector.start_server, args=('localhost', 9876, MessageHandler.get_messages_history()),
                     daemon=True).start()


peer_id = "renegade"
broadcast_and_listen(peer_id)

# TODO: Delete the comment regarding SSH to the VM before publishing!
# ssh -p 20462 jouda@dev.spsejecna.net  # s-kral5-2
# ssh -p 20475 jouda@dev.spsejecna.net  # s-kral5-3
# ssh -p 20110 jouda@dev.spsejecna.net  # molic-peer1
