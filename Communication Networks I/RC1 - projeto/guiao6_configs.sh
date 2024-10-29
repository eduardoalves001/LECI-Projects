#!/bin/bash

##### Configurações IPv4

#Na VirtualBox, alterar as configurações de adaptador da VM: só precisamos de 2 adaptadores: o 1º de NAT (o que nos permite aceder à Internet através do host), o 2ª de host-only ethernet adapter (ligação mais relevante no resto deste guião).
sudo ip link set enp0s8 up
sudo ip addr add 192.168.50.100/24 dev enp0s8

#No host, nas opções de adaptador, selecionar o adaptador correspondente à ligação entre VM e host, e definir o IP do host como 192.168.50.1/24, e o DNS como 192.168.50.100 (IP do nosso servidor)




##### DNS

sudo systemctl start bind9
#sudo systemctl status bind9




#São feitas as seguintes alterações ao documento /etc/bind/named.conf.local para criar uma zona:
#zone "arqredes.pt" in{
#	type master; //define the zone as master
#	file "/etc/bind/db.arqredes.pt"; //file with the domain records
#};




#Depois, é criado o documento /etc/bind/arqredes.pt, com a DNS em si:
#$TTL 604800
#$ORIGIN arqredes.pt.
#@ 	IN 	SOA 	ns1.arqredes.pt. adm.arqredes.pt. (
#			2 ; Serial
#			604800 ; Refresh
#			86400 ; Retry
#			2419200 ; Expire
#			604800) ; Negative Cache TTL
#	IN 	NS 	ns1.arqredes.pt.
#ns1	IN 	A 	192.168.50.100
#@ 	IN 	A 	192.168.50.100
#www 	IN 	A 	192.168.50.100
#siteA 	IN 	A 	192.168.50.100
#hostPC 	IN 	A 	192.168.50.1



cd /etc/bind
sudo named-checkzone arqredes.pt db.arqredes.pt


sudo systemctl restart bind9

#No PC host (o que iniciou este virtual), vamos a configurações de rede e mudamos o DNS server
#da rede a que estamos ligados para o DNS server que acabámos de configurar
#(192.169.50.100, que é o IP do PC virtual, que agora é o servidor)


#sudo systemctl status apache2
#sudo apt-get update
#sudo apt-get install apache2

sudo systemctl start apache2
#sudo systemctl status apache2

#No host ou na VM, realizar os seguintes comandos e ver se existe translação de nome para IP:
nslookup arqredes.pt
nslookup www.arqredes.pt
nslookup siteA.arqredes.pt
nslookup hostPC.arqredes.pt



##### HTTP
#Verificar se o serviço apache2 está instalado:
#sudo systemctl status apache2
#sudo apt-get update
#sudo apt-get install apache2


#iniciar serviço HTTP
sudo systemctl start apache2


#No host, iniciar um browser e aceder aos seguintes sites:
#192.168.50.100
#arqredes.pt
#www.arqredes.pt
#siteA.arqredes.pt



#Criar uma pasta "arqredes.pt-80" na pasta /var/www/html, e nessa pasta, criar uma página index.html. Esta página pode ser personalizada.
#Para que esta página seja mostrada ao aceder a "arqredes.pt", é preciso definir um novo host de apache2; 
#-para isso, cria-se na pasta /etc/apache2/sites-available/ um ficheiro "arqredes.pt-80.conf" com o conteúdo:
#<VirtualHost *:80>
#	DocumentRoot /var/www/html/arqredes.pt-80
#	ServerName arqredes.pt
#	ServerAlias www.arqredes.pt
#</VirtualHost>

#Inicializar o site e dar restart ao servidor apache:
sudo a2ensite arqredes.pt-80
sudo systemctl restart apache2







##### TFTP
#Verificar se o serviço TFTP está instalado
#sudo systemctl service atftpd
#sudo apt-get install atftpd

#No ficheiro /etc/default/atftpd, alterar a linha "USE_INET=true" para "USE_INET=false"

#Inicializar serviço TFTP
sudo systemctl start atftpd

#Verificar se está tudo bem
sudo systemctl status atftpd

#(caso haja algum erro de active(exited), é provável que se deva a outro serviço a usar a porta 69. Reiniciar a VM pode resolver isto.

#No servidor TFTP (pasta /srv/tftp/), criar 2 ficheiros para serem enviados para o host:
sudo su
cd /srv/tftp
dd if=/dev/urandom of=file1500 bs=1 count=1500
dd if=/dev/urandom of=file1024 bs=1 count=1024
chown nobody:nogroup *
exit


#No host, iniciar um terminal e executar os seguintes comandos (talvez seja necessário inicializar o TFTP client nas funcionalidades do Windows no Painel de Controlo):
#tftp -i 192.168.50.100 GET file1500
#tftp -i 192.168.50.100 GET file1024
#tftp -i 192.168.50.100 PUT file1500
#tftp -i 192.168.50.100 PUT file1024
#Caso não haja transferência de ficheiros, desativar firewall na rede privada (onde está a rede entre o host e a VM)





##### FTP
#Instalar pacote vsftpd
#Modificar o ficheiro /etc/vsftpd.conf (descomentar a linha do write_enable="YES")

#(na máquina virtual) sudo dd if=/dev/urandom of=file15k bs=1k count=15
#(no host era pedida uma password para usar o ftp, pelo que não foi possível terminar esta parte)