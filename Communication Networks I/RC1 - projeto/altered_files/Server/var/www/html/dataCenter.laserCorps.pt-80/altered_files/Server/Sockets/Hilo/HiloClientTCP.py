import socket
import signal
import sys




def signal_handler(sig, frame):
    print('\nDone!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Prima Ctrl+C, ou dê Enter sem escrever nada para terminar o programa.')




def input_validator(linha):
    try:
        num = int(linha)
        return True
    except:
        print("Input inválido. Tente Novamente.")
        return False





ip_addr = "198.137.170.196"                               #IP do servidor a que queremos conectar
tcp_port = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ip_addr, tcp_port))

dor=False



try:
    welcome=sock.recv(4096).decode()
    print(welcome)
except:
    ...

while True:
    try:
        while dor==False:
            message=input("Indique um número, e saberá de seguida se acertou ou não:")
            if input_validator(message)==True:
                dor=True
        
        message=message.encode()

        if len(message)>=1:
            sock.send(message)
            response = sock.recv(4096).decode()
            print('Server response: {}\n'.format(response))
            if response[0]=="Y":
                print("\nVitória!")
                sys.exit(0)
        elif len(message)==0:
            print("Terminando sessão. Adeus!")  #Terminar sessão sem recorrer ao Ctrl+C
            sys.exit(0)

        dor=False

    except (socket.timeout, socket.error):
        print('Erro do servidor. Terminado!')
        sys.exit(0)
