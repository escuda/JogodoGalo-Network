#SERVIDOR

import socket
import sys
l=[]
utilizadores = {}
usergamestate={}
Server_Port = 5005
available="available"
navailable="not available"
convidou=""
ServerSock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)	
ServerSock.bind(('',Server_Port))	

port, addr1 = ServerSock.recvfrom(100)

def verifica_lista(data):
	y = 0
	
	key= utilizadores.keys()
	while y < len(key):
		x = key[y]
		print "passa"
		print x
		y = y +1
		if x==data:
			ServerSock.sendto("Nome de registo existente",(ClientIP, int(port)))
			return 0
		
	return 1				

def verifica_convidado(nome):
	y = 0
	
	key= utilizadores.keys()
	while y < len(key):
		x = key[y]
		y = y +1
		print "x:"+x
		print "nome:"+nome
		if x==nome:
			return 1
		
	return 0	


while 1:
	print convidou
	print str(utilizadores)
	print str(utilizadores.keys())
	print str(utilizadores.values())
 	(comandoCliente, (ClientIP, port)) = ServerSock.recvfrom (100)
 	print comandoCliente
	
 	if comandoCliente in "listar":

 		ServerSock.sendto(str(usergamestate.items()),(ClientIP, int(port)))

	elif comandoCliente in "registar":
		(nomeutilizador, (ClientIP, port)) = ServerSock.recvfrom (100)
		
		if (verifica_lista(nomeutilizador)==1):

   			utilizadores[nomeutilizador] = port
   			usergamestate[nomeutilizador]= available
   			ServerSock.sendto("Registo Confirmado",(ClientIP, int(port)))

   	elif comandoCliente in "convida":
   		(convidar, (ClientIP, port)) = ServerSock.recvfrom (100)
   		print ("convidar="+convidar)
   		if(verifica_convidado(convidar)==0):
   			ServerSock.sendto("Jogador nao existe",(ClientIP, int(port)))
   		elif usergamestate[convidar]==navailable:
   			ServerSock.sendto("Jogador ocupado",(ClientIP, int(port)))
   		else:
   			convidou=utilizadores.keys()[utilizadores.values().index(port)]
   			convidare = utilizadores[convidar]
   			Wport=port
   			ServerSock.sendto("Convite Enviado",(ClientIP, int(port)))
   			ServerSock.sendto(("Convite Enviado por "+convidou+" : Aceita (a) ou Recusa (r)?"),(ClientIP, int(convidare)))

	elif comandoCliente in "convite aceite":
		usergamestate[convidou]=navailable
		usergamestate[convidar]=navailable
		print ("jogadores em uso: "+str(usergamestate))
		ServerSock.sendto("Convite aceite",(ClientIP, int(Wport)))
		ServerSock.sendto("A iniciar jogo",(ClientIP, int(Wport)))

	elif comandoCliente in "convite rejeitado":
		ServerSock.sendto("convite rejeitado",(ClientIP, int(Wport)))


	elif comandoCliente in "jogar":
		(posicao, (ClientIP, port)) = ServerSock.recvfrom (100)
		print posicao
		
		print str(port)

		if port == int(Wport):
			(estado_jogo, (ClientIP, port)) = ServerSock.recvfrom (100)
			print estado_jogo
			if estado_jogo == "ganhei":
				ServerSock.sendto("",(ClientIP, int(convidare)))
				ServerSock.sendto("perdeste",(ClientIP, int(convidare)))
			ServerSock.sendto(posicao,(ClientIP, int(convidare)))
			ServerSock.sendto(estado_jogo,(ClientIP, int(convidare)))

		elif port == int(convidare):
			print posicao
			ServerSock.sendto(posicao,(ClientIP, int(Wport)))	

	elif comandoCliente in "perdi":
		ServerSock.sendto("",(ClientIP, int(convidare)))
		ServerSock.sendto("ganhaste",(ClientIP, int(convidare))) 
	
	elif comandoCliente in "empate":
		ServerSock.sendto("",(ClientIP, int(convidare)))
		ServerSock.sendto("empate",(ClientIP, int(convidare)))

	elif comandoCliente in "jogo acabado":
		usergamestate[convidou]=available
		usergamestate[convidar]=available
		print ("jogadores em uso: "+str(usergamestate))
		estado_jogo=""
	elif comandoCliente in "termino":
		portremove=port
		if portremove in utilizadores.values():
			del usergamestate[usergamestate.keys()[utilizadores.values().index(port)]]
			del utilizadores[utilizadores.keys()[utilizadores.values().index(port)]]
	
		print str(utilizadores)
		ServerSock.sendto("a encerrar sessao...",(ClientIP, int(portremove)))

ServerSock.close()

