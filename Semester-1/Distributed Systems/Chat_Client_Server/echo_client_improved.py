import socket
import echo_protocol as echo
 
IP = '127.0.0.1'
PORT = 5000
 
print("Welcome to Echo Client!")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((IP, PORT))

sock_wrapper = echo.SocketWrapper(sock)
msg = "Hello there!"
sock_wrapper.send_msg(msg)
rcvd = sock_wrapper.recv_msg()
print(f'received: {rcvd}')

sock_wrapper.send_msg("Some more")
sock_wrapper.send_msg("messages")

rcvd = sock_wrapper.recv_msg()
print(f'received: {rcvd}')
rcvd = sock_wrapper.recv_msg()
print(f'received: {rcvd}')

sock.close()
