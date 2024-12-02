import zmq
import threading

# Server configuration
HOST = '127.0.0.1'  # Localhost
PORT = 5555         # Port number for communication

# List to keep track of connected clients
connected_clients = []  # List of tuples (username, client_id)

def handle_client_messages(socket, client_id, username):
    #Continuously listen for messages from a client and broadcast them.
    while True:
        try:
            # Receive a message from the client
            message = socket.recv_multipart()
            sender_id, msg = message
            msg = msg.decode('utf-8')
            if msg:
                broadcast_message = f"{username}: {msg}"
                print(broadcast_message)
                # Broadcast the message to all connected clients
                broadcast_to_clients(socket, sender_id, broadcast_message)
            else:
                print(f"Received empty message from {username}")
        except zmq.ZMQError:
            print(f"Connection with {username} lost")
            remove_client(username)
            break

def broadcast_to_clients(socket, sender_id, message):
    #Send a message to all connected clients except the sender.
    for client in connected_clients:
        client_username, client_id = client
        if client_id != sender_id:
            try:
                socket.send_multipart([client_id, message.encode('utf-8')])
            except zmq.ZMQError:
                print(f"Failed to send message to {client_username}")
                remove_client(client_username)

def remove_client(username):
    #Remove a client from the list of connected clients.
    global connected_clients
    connected_clients = [client for client in connected_clients if client[0] != username]
    print(f"{username} has been removed from the chat")

def main():
    #Main function to start the chat server.
    context = zmq.Context()
    router_socket = context.socket(zmq.ROUTER)
    router_socket.bind(f"tcp://{HOST}:{PORT}")
    print(f"Server started at {HOST}:{PORT}")

    while True:
        # Wait for the next request from a client
        try:
            message = router_socket.recv_multipart()
            client_id, empty, content = message
            content = content.decode('utf-8')

            if content.startswith("USERNAME:"):
                username = content.split("USERNAME:")[1]
                connected_clients.append((username, client_id))
                print(f"{username} has joined the chat")
                welcome_msg = f"{username} has joined the chat"
                broadcast_to_clients(router_socket, client_id, welcome_msg)
                # Start a new thread to listen for messages from this client
                threading.Thread(target=handle_client_messages, args=(router_socket, client_id, username), daemon=True).start()
        except zmq.ZMQError:
            print("An error occurred with the server socket")
            break

if __name__ == '__main__':
    main()
