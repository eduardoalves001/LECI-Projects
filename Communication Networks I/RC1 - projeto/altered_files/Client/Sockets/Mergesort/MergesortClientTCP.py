import socket
import signal
import sys




def signal_handler(sig, frame):
    print('\nDone!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to exit, or enter an empty or very short (1 char long) message...')




def input_validator(linha):
    numeros=linha.split()
    for num in numeros:
        try:
            a = int(num)
        except:
            print("Input inválido. Tente novamente.")
            return False
    return True





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
            message=input("Conjunto de números que deseja ordenar (separados por whitespace)? ")
            if input_validator(message)==True:
                dor=True
        
        message=message.encode()

        if len(message)>=1:
            sock.send(message)
            response = sock.recv(4096).decode()
            print('Server response: {}'.format(response))
        elif len(message)==0:
            print("Terminando sessão. Adeus!")  #Terminar sessão sem recorrer ao Ctrl+C
            sys.exit(0)

        dor=False

    except (socket.timeout, socket.error):
        print('Erro do servidor. Terminado!')
        sys.exit(0)
