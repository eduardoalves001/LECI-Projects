import socket
import signal
import sys

def signal_handler(sig, frame):
    print('\nDone!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to exit, or enter an empty or very short (1 char long) message...')








ip_addr = "198.137.170.196"                               #IP do servidor a que queremos conectar
tcp_port = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((ip_addr, tcp_port))





try:
    welcome=sock.recv(4096).decode()
    print(welcome)
except:
    ...

while True:
    try: 
        message=input("Message to send? ").encode()
        if len(message)>1:
            sock.send(message)
            response = sock.recv(4096).decode()
            print('Server response: {}'.format(response))
        else:
            print("Terminating session. Bye!")  #Terminar sessão sem recorrer ao Ctrl+C
            sys.exit(0)
    except (socket.timeout, socket.error):
        print('Server error. Done!')
        sys.exit(0)

