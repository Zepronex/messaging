import zmq
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Server configuration
HOST = '127.0.0.1'  # Change to the server's IP address if needed
PORT = 5555

# GUI configuration
BG_COLOR = '#2C2F33'
TEXT_COLOR = '#FFFFFF'
FONT = ('Verdana', 12)
BUTTON_FONT = ('Verdana', 10)
SMALL_FONT = ('Verdana', 10)

def update_chat_window(message):
    # Display a message in the chat window.
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, message + '\n')
    chat_display.config(state=tk.DISABLED)
    chat_display.see(tk.END)

def connect_to_server():
    # Connect to the server and start listening for messages.
    username = username_entry.get()
    if username:
        try:
            # Connect to the server
            context = zmq.Context()
            socket = context.socket(zmq.DEALER)
            identity = username.encode('utf-8')
            socket.setsockopt(zmq.IDENTITY, identity)
            socket.connect(f"tcp://{HOST}:{PORT}")

            # Send the username to the server
            socket.send_multipart([b'', f"USERNAME:{username}".encode('utf-8')])

            # Disable the username entry and button
            username_entry.config(state=tk.DISABLED)
            connect_button.config(state=tk.DISABLED)

            # Start a thread to listen for messages
            threading.Thread(target=receive_messages, args=(socket,), daemon=True).start()
        except zmq.ZMQError:
            messagebox.showerror("Connection Error", f"Cannot connect to server at {HOST}:{PORT}")
    else:
        messagebox.showerror("Invalid Username", "Please enter a username")

def send_message():
    #Send a message to the server.
    message = message_entry.get()
    if message:
        try:
            # Send the message to the server
            context = zmq.Context.instance()
            socket = context.socket(zmq.DEALER)
            identity = username_entry.get().encode('utf-8')
            socket.setsockopt(zmq.IDENTITY, identity)
            socket.connect(f"tcp://{HOST}:{PORT}")
            socket.send_multipart([b'', message.encode('utf-8')])
            message_entry.delete(0, tk.END)
        except zmq.ZMQError:
            messagebox.showerror("Send Error", "Failed to send message to the server")
    else:
        messagebox.showerror("Empty Message", "Cannot send an empty message")

def receive_messages(socket):
    # Continuously listen for messages from the server.
    while True:
        try:
            message = socket.recv_multipart()
            _, content = message
            content = content.decode('utf-8')
            if content:
                update_chat_window(content)
            else:
                messagebox.showerror("Error", "Received empty message from server")
        except zmq.ZMQError:
            break

def on_close():
    # Handle the window close event
    context = zmq.Context.instance()
    context.term()
    root.destroy()

# Create the main application window
root = tk.Tk()
root.title("Chat Application")
root.geometry("600x500")
root.configure(bg=BG_COLOR)

# Username frame
username_frame = tk.Frame(root, bg=BG_COLOR)
username_frame.pack(pady=10)

username_label = tk.Label(username_frame, text="Username:", font=FONT, bg=BG_COLOR, fg=TEXT_COLOR)
username_label.pack(side=tk.LEFT, padx=5)

username_entry = tk.Entry(username_frame, font=FONT)
username_entry.pack(side=tk.LEFT, padx=5)

connect_button = tk.Button(username_frame, text="Connect", font=BUTTON_FONT, command=connect_to_server)
connect_button.pack(side=tk.LEFT, padx=5)

# Chat display
chat_display = scrolledtext.ScrolledText(root, font=SMALL_FONT, bg='#23272A', fg=TEXT_COLOR, state=tk.DISABLED)
chat_display.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

# Message entry
message_frame = tk.Frame(root, bg=BG_COLOR)
message_frame.pack(pady=10)

message_entry = tk.Entry(message_frame, font=FONT, width=40)
message_entry.pack(side=tk.LEFT, padx=5)

send_button = tk.Button(message_frame, text="Send", font=BUTTON_FONT, command=send_message)
send_button.pack(side=tk.LEFT, padx=5)

root.protocol("WM_DELETE_WINDOW", on_close)

def main():
    root.mainloop()

if __name__ == '__main__':
    main()
