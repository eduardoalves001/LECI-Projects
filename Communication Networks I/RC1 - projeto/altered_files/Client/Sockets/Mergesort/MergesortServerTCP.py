import socket
import threading
import signal
import sys



def merge_sort(lista):
    if len(lista)==1:
        return lista
        
    meio = len(lista)//2
    cena = merge_sort(lista[0:meio])
    dor = merge_sort(lista[meio:])

    coisa=[]
    i=0
    index=0

    while index < len(cena) and i < len(dor):       
        if cena[index]<=dor[i]:
            coisa.append(cena[index])
            index+=1
        else:
            coisa.append(dor[i])
            i+=1

    if index < len(cena):
        for index2 in range(index, len(cena)):
            coisa.append(cena[index2])

    if i < len(dor):
        for i2 in range(i, len(dor)):
            coisa.append(dor[i2])

    return coisa






def signal_handler(sig, frame):
    print('\nDone!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to exit...')







def handle_client_connection(client_socket,address): 
    print('Accepted connection from {}:{}'.format(address[0], address[1]))
    try:
        while True:
            request = client_socket.recv(1024)
            if not request:
                client_socket.close()
            else:
                msg=request.decode()

                
                listaNumerica=[]
                listaPalavras=msg.split()
                for palavra in listaPalavras:
                    try:
                        listaNumerica.append(int(palavra))
                    except:
                        print("Input inválido.")
                        break

                listaOrdenada=merge_sort(listaNumerica)
                print("Lista Ordenada:", listaOrdenada)

                msg=''
                for num in listaOrdenada:
                    msg+=str(num)+" "
                msg=msg.encode()
                client_socket.send(msg)
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
        
        


        msg="Benvindo! Eu sou o servidor {}.\nO meu IP é: {}.\nProvidencie-me um conjunto de números, e eu devolvo-o ordenado de forma crescente.".format(nomeServer, ipServer)
        msg+="\n"
        client_sock.send((msg).encode())

        client_handler = threading.Thread(target=handle_client_connection,args=(client_sock,address),daemon=True)
        client_handler.start()





main()

