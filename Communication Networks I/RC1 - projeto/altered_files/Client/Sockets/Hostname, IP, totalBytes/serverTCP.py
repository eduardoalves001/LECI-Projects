import datetime
import os
import socket
import threading
import signal
import sys

def signal_handler(sig, frame):
    print('\nDone!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to exit...')







def handle_client_connection(client_socket,address, dicioClientes, totalBytes): 
    print('Accepted connection from {}:{}'.format(address[0], address[1]))
    try:
        while True:
            request = client_socket.recv(1024)
            if not request:
                client_socket.close()
            else:
                msg=request.decode()

                
                tamanho=len(request)
                totalBytes["totalBytes"]+=tamanho                         #Adicionar tamanho da mensagem recebida a totalBytes
                if address not in dicioClientes:            #Adicionar/atualizar entrada no dicionário do cliente com os bytes recebidos
                    dicioClientes[address]=tamanho              
                else:
                    dicioClientes[address]+=tamanho          


                print('Received {}'.format(msg))
                #msg=("ECHO: "+msg).encode()
                msg=''+'Total Bytes received: '+str(totalBytes["totalBytes"])+'\n'
                for cliente in dicioClientes.keys():
                    msg+="\n   IP {}: {} bytes".format(cliente, dicioClientes[cliente])
                msg+="\n"
                msg=(msg).encode()


                client_socket.send(msg)
    except (socket.timeout, socket.error):
        print('Client {} error. Done!'.format(address))

        #fazer um log da sessão na pasta onde se encontra o serviDor
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        with open("log.txt",  'a', encoding="utf-8") as stream:
            stream.write(str(datetime.datetime.now())+"\n")
            for chave, valor in dicioClientes.items():
                try:
                    stream.write("\tIP {}:   {} bytes\n".format(chave, valor))
                except:
                    continue
            stream.write("Total Bytes: "+str(totalBytes["totalBytes"]))
            stream.write("\n\n\n")





ip_addr = "0.0.0.0"
tcp_port = 5005

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #criar objeto socket. AF_INET: IPv4; SOCK_STREAM: TCP
server.bind((ip_addr, tcp_port))                            #ligar esse socket a qualquer IP (cliente) que tente ligar no porto 5005
server.listen(5)  # max backlog of connections              #server pode ouvir/ligar a 5 clientes em simultâneo no máximo

print('Listening on {}:{}'.format(ip_addr, tcp_port))






def main():
    nomeServer = socket.gethostname()                           #nome do servidor
    ipServer = socket.gethostbyname(nomeServer)                 #IP do servidor
    dicioClientes={}                                            #dicionário com par chave:valor = clientes: bytes enviados
    totalBytes={}                                               #total de bytes recebidos. Como se está a usar threads, e não há maneira óbvia de dar return do client_handler abaixo, usa-se um dicionário para guardar este valor
    totalBytes["totalBytes"]=0



    while True:                                                 #server está a ouvir para sempre (ou até o servidor ser desligado)
        client_sock, address = server.accept()                  #qualquer cliente que se conecte é aceite
        
        


        msg="Benvindo ao servidor {}.\nO IP deste servidor é: {}.\nAté ao presente momento, recebi {} bytes de dados:".format(nomeServer, ipServer, totalBytes["totalBytes"])
        #client_sock.send(("Benvindo ao servidor {}.\nO IP deste servidor é: {}.\nAté ao presente momento, recebi {} bytes de dados:".format(nomeServer, ipServer, totalBytes["totalBytes"])).encode())
        for cliente in dicioClientes.keys():
            #client_sock.send(("\n   IP {}: {} bytes".format(cliente, dicioClientes[cliente])).encode())
            msg+="\n   IP {}: {} bytes".format(cliente, dicioClientes[cliente])
        msg+="\n"
        #client_sock.send(("\n").encode())
        client_sock.send((msg).encode())



        client_handler = threading.Thread(target=handle_client_connection,args=(client_sock,address, dicioClientes, totalBytes),daemon=True)
        client_handler.start()





main()

