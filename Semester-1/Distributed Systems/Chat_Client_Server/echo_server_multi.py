import socket
import threading
import echo_protocol as echo
 
print("Welcome to Echo Server!")

IP = '127.0.0.1'
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((IP, echo.PORT))
sock.listen()

def handle_client(client_socket, client_address):
    print(f"Thread for handling client: {client_address}")
    sock_wrapper = echo.SocketWrapper(client_socket)

    while True:
        rcvd = sock_wrapper.recv_msg()
        if rcvd is None:
            client_sock.close()
            break
        sock_wrapper.send_msg(rcvd)
 
while True:
    print("Ready to accept a client connection.")
    client_sock, addr = sock.accept()
    print(f"Accepted new client connection: {addr}")
    th = threading.Thread(target=handle_client, args=(client_sock, addr), daemon=True)
    th.start()
