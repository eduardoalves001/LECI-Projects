import datetime
import os, glob
import socket
import threading
import signal
import sys

def signal_handler(sig, frame):
    print('\nDone!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to exit...')







def handle_client_connection(client_socket,address, libraria): 
    print('Accepted connection from {}:{}'.format(address[0], address[1]))
    try:


        nomeServer = socket.gethostname()                           #nome do servidor
        ipServer = socket.gethostbyname(nomeServer)                 #IP do servidor
        msg="Benvindo ao servidor {}.\nO IP deste servidor é: {}.\nProvidencie-me o nome de um ficheiro, e eu tentarei encontrar um ficheiro com esse nome na minha libraria e entregar-lho\n".format(nomeServer, ipServer)
        client_socket.send((msg).encode())


        while True:
            request = client_socket.recv(1024)
            if not request:
                client_socket.close()
            else:
                msg=request.decode()
                nomeFicheiro=msg

                numFiles, dicioFiles = libraria_pesquisaDor(msg, libraria)

                if numFiles==0:
                    msg = "[No transfer] Não encontrámos nenhum ficheiro que corresponda à sua pesquisa.\n"
                elif numFiles==1 and dicioFiles[1]==msg:
                    msg=''
                    with open(dicioFiles[1], 'rb') as stream:
                        size=0
                        #fileTemp=b''
                        fileTemp=bytearray()
                        dor=stream.read(29)
                        #print(dor.decode())
                        while dor:
                            fileTemp.extend(dor)
                            size+=len(dor)
                            if size>1000:
                                print("Ficheiro é demasiado grande.")
                                return
                            dor=stream.read(29)
                            #print(dor.decode())

                    msg+=fileTemp.decode()
                    print("Ficheiro preparado para envio: "+nomeFicheiro+"\nConteúdo:")
                    


                else:
                    msg = "[No transfer] Foram encontrados os seguintes ficheiros que correspondem à sua pesquisa:\n"
                    for file in dicioFiles.keys():
                        msg+="\t"+dicioFiles[file]+"\n"

                print(msg)

                msg+='~' #hieroglifo egípcio adicionado ao fim de cada mensagem; se o cliente ler este símbolo, pode terminar a "espera" do sock.recv() por mais mensagens. Edit: não sei representar esse símbolo em código UTF-8, mas ele também é composto por 4 bytes em UTF-8. ~ é composto por 1 byte apenas (e na stream do cliente, podemos verificar sempre 1 byte em segurança)

                msg=msg.encode()
                client_socket.send(msg)
                #client_socket.close()       #essencial para que o cliente saiba que a coneção já acabou (assim, o socl.recv() no cliente não fica à espera para sempre da próxima mensagem do server). Edit: afinal, a maneira de resolver isto é de no ciclo while True do cliente, que espera a stream do server, verificar se o tamanho da stream é menor que o do buffer. Isto porque, se o tamanho da stream recebida for menor que o do buffer, mas não for 0, significa que é o último "pacote" de dados que o server mandou. Se o server mandar um pacote com os dados finais que quer enviar, e o tamanho deste pacote for igual ao buffer, o server manda ainda um último pacote com 0 bytes de dados, só para informar que terminou a stream. Edit2: com o método do edit1, não sabe quando acabou a stream =( )
                

    except (socket.timeout, socket.error):
        print('Client {} error. Done!'.format(address))





ip_addr = "0.0.0.0"
tcp_port = 5005

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #criar objeto socket. AF_INET: IPv4; SOCK_STREAM: TCP
server.bind((ip_addr, tcp_port))                            #ligar esse socket a qualquer IP (cliente) que tente ligar no porto 5005
server.listen(5)  # max backlog of connections              #server pode ouvir/ligar a 5 clientes em simultâneo no máximo

print('Listening on {}:{}'.format(ip_addr, tcp_port))





def libraria_pesquisaDor(nome, pasta):
    if os.path.isdir(pasta)==False:
        print("A libraria não é uma pasta.")
        exit(29)

    numFiles = 0
    dicioFiles = {}
    
    os.chdir(pasta)
    #print(nome)
    for file in glob.glob("*"+nome+"*"):
        numFiles+=1
        dicioFiles[numFiles] = file
        #print(file)

    return numFiles, dicioFiles





def main():

    libraria = os.path.dirname(os.path.abspath(__file__))


    while True:                                                 #server está a ouvir para sempre (ou até o servidor ser desligado)
        client_sock, address = server.accept()                  #qualquer cliente que se conecte é aceite
        


        client_handler = threading.Thread(target=handle_client_connection,args=(client_sock,address, libraria),daemon=True)
        client_handler.start()





main()

