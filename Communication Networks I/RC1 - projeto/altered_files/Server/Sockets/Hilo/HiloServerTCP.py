import socket
import threading
import signal
import sys
import random





def signal_handler(sig, frame):
    print('\nDone!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to exit...')







def handle_client_connection(client_socket,address): 
    print('Accepted connection from {}:{}'.format(address[0], address[1]))
    try:
        secret = random.randrange(1, 101);
        print("The special number is:", secret)
        while True:
            request = client_socket.recv(1024)
        

            if not request:
                client_socket.close()
            else:
                msg=request.decode()

                try:
                    number=int(msg)
                except:
                    print("=(")
                    break

                if number < secret:
                    msg="The chosen number is too small, try again."
                elif number > secret:
                    msg="The chosen number is too big, try again."
                elif number == secret:
                    msg="You have correctly guessed the secret!"
                    print("Client correctly guessed the number!")
                else:
                    print("Something dark and ominous is at play here. Is is well beyond the known horrors of this world. Do not feel it, for it is far worse than any pain you have experienced. Cena dor.")
                    exit(29)

                
                msg=msg.encode()
                client_socket.send(msg)

                if number == secret:
                    break
                
    except (socket.timeout, socket.error):
        print('Client {} error. Done!'.format(address))





ip_addr = "0.0.0.0"
tcp_port = 5005

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #criar objeto socket. AF_INET: IPv4; SOCK_STREAM: TCP
server.bind((ip_addr, tcp_port))                            #ligar esse socket a qualquer IP (cliente) que tente ligar no porto 5005
server.listen(5)  # max backlog of connections              #server pode ouvir/ligar a 5 clientes em simultâneo no máximo

print('Listening on {}:{}'.format(ip_addr, tcp_port))






def main():
    nomeServer = socket.gethostname()                           #nome do servidor
    ipServer = socket.gethostbyname(nomeServer)                 #IP do servidor



    while True:                                                 #server está a ouvir para sempre (ou até o servidor ser desligado)
        client_sock, address = server.accept()                  #qualquer cliente que se conecte é aceite
        
        


        msg="Hi! I'm {}, and my IP is {}.\nCan you guess my secret?\n".format(nomeServer, ipServer)
        client_sock.send((msg).encode())

        client_handler = threading.Thread(target=handle_client_connection,args=(client_sock,address),daemon=True)
        client_handler.start()





main()

