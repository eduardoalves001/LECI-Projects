import os
import socket
import signal
import sys

def signal_handler(sig, frame):
    print('\nDone!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to exit, or enter an empty or very short (1 char long) message...\n\n')








ip_addr = "127.0.0.1"                               #IP do servidor a que queremos conectar
tcp_port = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((ip_addr, tcp_port))

#sock.setblocking(0)
fileFlag=False
noTransfer='[No transfer]'
number=0
numStream=0
os.chdir(os.path.dirname(os.path.abspath(__file__)))




try:
    welcome=sock.recv(4096).decode()
    print(welcome)
except:
    ...

while True:
    #try: 
        message=input("Message to send? ").encode()
        if len(message)>=1:
            #enviar mensagem, e esperar pela resposta com o sock.recv()
            sock.send(message)


            #receber a stream de dados, e meter flag de ficheiro a False
            msg=''
            fileTemp=bytearray()
            fileFlag=False
            numStream=0


            while True:

                sock.settimeout(3)     #impede espera infinita

                response = sock.recv(29)
                responseDecoded = response.decode('utf-8', 'ignore')

                #verificar se a stream é para ser guardada
                if fileFlag==False and numStream==0:
                    if responseDecoded[0:len(noTransfer)]==noTransfer:
                        ...
                    else:
                        print("A guardar ficheiro...")
                        fileFlag=True
                

                if responseDecoded[-1]=='~':
                    msg+=responseDecoded[:-1]
                    if fileFlag==True:
                        #print(response[-1])
                        fileTemp.extend(response[:-1])
                    break
                else:
                    if fileFlag==True:
                        #print(response)
                        fileTemp.extend(response)
                

                numStream+=1
                msg+=responseDecoded
                #if len(response)<29:        #é essencial que este check seja feito no final para que toda a mensagem seja composta antes de sair do ciclo, e é mais essencial ainda que o tamanho que se está a verificar seja comparado com o mesmo tamanho que o buffer (29, neste caso). Edit: mesmo assim, não sabe quando é que acabou a stream =( )
                #    break

                
                
            if fileFlag==True:
                with open('file'+str(number), 'wb') as stream:
                        stream.write(fileTemp)
                number+=1

            print('Server response: {}'.format(msg))
        else:
            print("Terminating session. Bye!")  #Terminar sessão sem recorrer ao Ctrl+C
            sys.exit(0)
    #except (socket.timeout, socket.error):
    #    print('Server error. Done!')
    #    sys.exit(0)



#é preciso uma maneira (do lado do servidor) de informar o cliente para guardar o que recebeu. O cliente precisa de fazer um open(msg) as algo para guardar o que recebeu.