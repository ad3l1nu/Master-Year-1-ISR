import socket
import echo_protocol as echo
import sys

IP = '127.0.0.1'
PORT = 5000

print("--- Echo Client Pro v1.0 ---")

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Setam un timeout pentru a nu astepta la infinit daca serverul e picat
    sock.settimeout(5) 
    sock.connect((IP, PORT))
    sock.settimeout(None) # Revenim la modul blocking pentru comunicare
    
    sock_wrapper = echo.SocketWrapper(sock)
    print(f"Conectat cu succes la {IP}:{PORT}")
    print("Scrie mesajul tau (sau 'exit' pentru a inchide):")

    while True:
        user_input = input("> ")
        
        if user_input.lower() == 'exit':
            break
            
        if not user_input:
            continue

        sock_wrapper.send_msg(user_input)
        rcvd = sock_wrapper.recv_msg()
        
        if rcvd:
            print(f"Serverul a raspuns: {rcvd}")
        else:
            print("Conexiunea cu serverul a fost pierdută.")
            break

except ConnectionRefusedError:
    print("Eroare: Nu s-a putut stabili conexiunea. Serverul este oprit.")
except Exception as e:
    print(f"A aparut o eroare neasteptata: {e}")
finally:
    sock.close()
    print("Conexiune inchisa. La revedere!")