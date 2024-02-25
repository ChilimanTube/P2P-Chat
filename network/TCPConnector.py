import socket
import threading
import json
from network import MessageHandler


def handle_client(connection, messages_history):
    try:
        print("TCP: |LISTENER|: Connection from", connection.getpeername())
        while True:
            data = connection.recv(1024)
            if not data:
                break
            message = json.loads(data.decode())
            command = message.get("command")
            if command == "hello":
                print("TCP: |LISTENER|: Received Hello command from", connection.getpeername())
                response = json.dumps({"status": "ok", "messages": messages_history}) + "\n"
                connection.sendall(response.encode())
                print("TCP: |LISTENER|: Sent:", response, "to", connection.getpeername())
                print("TCP: |LISTENER|: Handshake successful.")
                print("TCP: |LISTENER|: Number of messages stored:", MessageHandler.number_of_messages())
            elif command == "new_message":
                print("TCP: |LISTENER|: Received new message:", message["message"])
                messages_history[message["message_id"]] = {"peer_id": message["peer_id"], "message": message["message"]}
                response = json.dumps({"status": "ok"})
                connection.sendall(response.encode())
    finally:
        print("TCP: |LISTENER|: Closing connection with", connection.getpeername())
        connection.close()


def start_server(host, port, messages_history):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print("TCP: Server listening on", host, port)

    try:
        while True:
            client, address = server.accept()
            threading.Thread(target=handle_client, args=(client, messages_history)).start()
    finally:
        server.close()


def receive_complete_message(sock):
    buffer = ''
    while not buffer.endswith('\n'):
        data = sock.recv(1024).decode()
        if not data:
            break
        buffer += data
    return buffer.strip()


def send_hello(peer_address, peer_port, peer_id):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((peer_address, peer_port))
            hello_message = json.dumps({"command": "hello", "peer_id": peer_id}) + "\n"
            sock.sendall(hello_message.encode())
            print(f"TCP: |SENDER|: Sent hello message to {peer_address}:{peer_port}")
            response = receive_complete_message(sock)
            response_message = json.loads(response)
            if response_message.get("status") == "ok":
                print(f"TCP: |SENDER|: Received status OK from {peer_address}:{peer_port}")
                print("TCP: |SENDER|: Handshake successful.")
                print("TCP: |SENDER|: Fetching messages...")
                MessageHandler.update_local_history(response_message["messages"])
            else:
                print("TCP: |SENDER|: Handshake failed.")
    except Exception as e:
        print(f"TCP: |SENDER_ERROR|: Failed to establish connection: {e}")


def send_new_message(peer_address, peer_port, message_id, message, peer_id):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((peer_address, peer_port))
        new_message = json.dumps({"command": "new_message", "message_id": message_id,
                                  "message": message, "peer_id": peer_id})
        sock.sendall(new_message.encode())
        response = sock.recv(1024)
        print("TCP: Received:", response.decode())


def get_new_message():
    return ""
