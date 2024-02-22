import socket
import threading
import json


def handle_client(connection, messages_history):
    try:
        while True:
            data = connection.recv(1024)
            if not data:
                break
            message = json.loads(data.decode())
            command = message.get("command")
            if command == "hello":
                # Send back the history of messages as a response
                response = json.dumps({"status": "ok", "messages": messages_history})
                connection.sendall(response.encode())
            elif command == "new_message":
                # Add the new message to the history and acknowledge it
                messages_history[message["message_id"]] = {"peer_id": message["peer_id"], "message": message["message"]}
                response = json.dumps({"status": "ok"})
                connection.sendall(response.encode())
    finally:
        connection.close()


def start_server(host, port, messages_history):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)  # Listen for up to 5 connections
    print("TCP Server listening on", host, port)

    try:
        while True:
            client, address = server.accept()
            threading.Thread(target=handle_client, args=(client, address, messages_history)).start()
    finally:
        server.close()


def receive_complete_message(sock):
    buffer = ''
    while not buffer.endswith('\n'):
        data = sock.recv(1024).decode()
        if not data:
            break  # Connection closed
        buffer += data
    return buffer.strip()


def send_hello(peer_address, peer_port, peer_id):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((peer_address, peer_port))
            hello_message = json.dumps({"command": "hello", "peer_id": peer_id}) + "\n"
            sock.sendall(hello_message.encode())
            print(f"Sent hello message to {peer_address}:{peer_port}")
            response = receive_complete_message(sock)
            response_message = json.loads(response)
            if response_message.get("status") == "ok":
                print("Handshake successful.")
                handle_client(sock, {})
            else:
                print("Handshake failed.")
    except Exception as e:
        print(f"Failed to establish TCP connection: {e}")


def send_new_message(peer_address, peer_port, message_id, message, peer_id):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((peer_address, peer_port))
        new_message = json.dumps({"command": "new_message", "message_id": message_id, "message": message, "peer_id": peer_id})
        sock.sendall(new_message.encode())
        response = sock.recv(1024)
        print("Received:", response.decode())
