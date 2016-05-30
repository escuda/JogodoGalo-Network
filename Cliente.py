#CLIENTE

import socket, random, os, time, threading, signal
import sys


fecha = True
registo = False
check=0
Server_Port = 5005
board= ['1','2','3','4','5','6','7','8','9']
resultado=""
empate=0
estado_jogo="a jogar"
jogo= True
jogadas=0

ClientSock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)	

while check==0:
	PORT= random.randint(6000,10000)
	print PORT
	print "passa"
	command=("netstat -l | grep "+str(PORT))
	if os.system(command)==0:
		check=0
	else:
		check=1
def signal_handler(signum, frame):
    raise Exception("Timed out!")

sockread= socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sockread.bind(('127.0.0.1', PORT))
ClientSock.sendto(str(PORT), ('127.0.0.1', Server_Port))

def desenha_jogo():
	print board[0], "|", board[1], "|", board[2]
	print ("---------")
	print board[3], "|", board[4], "|", board[5]
	print ("---------")
	print board[6], "|", board[7], "|", board[8]

def jogada(posicao):
	if board[posicao-1]=="x" or board[posicao-1]=="o" :
		print "jogada invalida"
		return 0
	else:
		board[posicao-1]="x"
	return 1

def jogada_adv(posicao):
	board[posicao-1]="o"
	return

def check_empate():
	global empate
	if jogadas>8 and resultado=="":
		return 1
	return 0




def check_vitoria():
	global resultado
	if board[0]==board[1]==board[2]:
		resultado=board[0]
	elif board[3]==board[4]==board[5]:
		resultado=board[3]
	elif board[6]==board[7]==board[8]:
		resultado=board[6]
	elif board[0]==board[3]==board[6]:
		resultado=board[0]
	elif board[1]==board[4]==board[7]:
		resultado=board[1]
	elif board[2]==board[5]==board[8]:
		resultado=board[2]
	elif board[0]==board[4]==board[8]:
		resultado=board[0]
	elif board[2]==board[4]==board[6]:
		resultado=board[2]
	else:
		resultado=""
	return resultado

def check_vencedor():
	global estado_jogo
	check_vitoria()
	print resultado
	if resultado=="x":
		estado_jogo="ganhei"
		sockread.sendto(estado_jogo,('127.0.0.1',Server_Port))
		print estado_jogo

	elif resultado=="o":
		estado_jogo="perdi"
		sockread.sendto(estado_jogo,('127.0.0.1',Server_Port))
		print estado_jogo
    	
	else:
		if check_empate()==1:
			estado_jogo="empate"
			sockread.sendto(estado_jogo,('127.0.0.1',Server_Port))
			print estado_jogo
		else:
			sockread.sendto(estado_jogo,('127.0.0.1',Server_Port))
			print estado_jogo
	return jogo

def jogar():
	global jogo
	global jogadas
	jogadas=0
	while jogo==True:
		jogadavalida=0
		print "Voce e o simbolo:x"
		desenha_jogo()
		check_vencedor()
		if estado_jogo!="a jogar":
			jogo= False
			break
		while jogadavalida==0:
			posicao= int(raw_input("E a sua vez de jogar, introduza casa: "))
			jogadavalida=jogada(posicao)
		jogadas=jogadas+2
		print str(jogadas)
		sockread.sendto("jogar",('127.0.0.1',Server_Port))
		sockread.sendto(str(posicao),('127.0.0.1',Server_Port))
		check_vencedor()
		if estado_jogo!="a jogar":

			jogo= False
			break
		else:
			print " espere pelo seu adversario..."
			(posicao_adv,(ServerIP,ServerPort)) = sockread.recvfrom (100)
			print posicao_adv
			jogada_adv(int(posicao_adv))
		jogo=True
		
	return

def termina():
	global fecha
	terminar = raw_input("Pretende sair (y/n):")
	if terminar == "y":
		sockread.sendto("termino",('127.0.0.1',Server_Port))
		(m,(ServerIP,ServerPort)) = sockread.recvfrom (100)
		print m
		fecha = False
	elif terminar == "n":
		fecha = True
	else:
		print ("Input incorreto!")
		terminar = raw_input("Pretende sair (y/n):")
		
	return


while fecha == True:
	

	print("|-----------|-------------------|" )
	print("|  Comando  |       Funcao      |")
	print("|-----------|-------------------|")
	print("|     1     |      Registar     |")
	print("|-----------|-------------------|")
	print("|     2     |  Listar Jogadores |")
	print("|-----------|-------------------|")
	print("|     3     | Convida Jogadores |")
	print("|-----------|-------------------|")
	print("|     4     | Caixa de mensagens|")
	print("|-----------|-------------------|")
	print("|     5     |    Fechar Jogo    |")
	print("|-----------|-------------------|")
	
	comando = raw_input("Introduza o Comando: ")

	if comando in "1":
		while registo == False:
			nome_Utilizador = raw_input("Registe o seu nome: ")
			sockread.sendto("registar",('127.0.0.1',Server_Port))
			sockread.sendto(nome_Utilizador,('127.0.0.1',Server_Port))
			(MensagemRegisto,(ServerIP,ServerPort)) = sockread.recvfrom (100)
			if MensagemRegisto == "Nome de registo existente":
				print MensagemRegisto
				nome_Utilizadornovo = raw_input("Registe o seu nome: ")
				sockread.sendto(nome_Utilizadornovo,('127.0.0.1',Server_Port))
				registo = False

			elif MensagemRegisto == "Registo Confirmado":
				registo = True

			print MensagemRegisto	
				
	elif comando in "2":
		sockread.sendto("listar",('127.0.0.1',Server_Port))	
		(Lista,(ServerIP,ServerPort)) = sockread.recvfrom (100)
		print Lista

	elif comando in "3":
		if registo==True:
			convidar = raw_input("Quem quer convidar: ")
			sockread.sendto("convida",('127.0.0.1',Server_Port))

			sockread.sendto(convidar,('127.0.0.1',Server_Port))	
			(msg,(ServerIP,ServerPort)) = sockread.recvfrom (100)	
			print msg
			if msg == "Jogador ocupado" or msg=="Jogador nao existe":
				print "a sair..."
			else:	
				wport=PORT+2
				
				(conv,(ServerIP,ServerPort)) = sockread.recvfrom (100)
				if conv=="Convite aceite":
					(msg,(ServerIP,ServerPort)) = sockread.recvfrom (100)
					print msg
					board= ['1','2','3','4','5','6','7','8','9']
					jogo=True
					estado_jogo="a jogar"
					resultado=""
					jogar()
					sockread.sendto(estado_jogo,('127.0.0.1',Server_Port))	
				else:
					sockread.sendto("jogo acabado",('127.0.0.1',Server_Port))
					fecha=True
					board= ['1','2','3','4','5','6','7','8','9']
	elif comando in "4":
		signal.signal(signal.SIGALRM, signal_handler)
		signal.alarm(1)
		try:
			
			(msg,(ServerIP,ServerPort)) = sockread.recvfrom (100)
			print msg
			if msg!=None:
				signal.alarm(40)
				print("recebeste um convite")
				answer=raw_input("Aceita o convite? ")
				if answer=="a":
					signal.alarm(0)
					board= ['1','2','3','4','5','6','7','8','9']
					jogo=True
					estado_jogo="a jogar"
					resultado=""
					sockread.sendto("convite aceite",('127.0.0.1',Server_Port))
					(posicao,(ServerIP,ServerPort))=sockread.recvfrom(100)
					(estado_jogo,(ServerIP,ServerPort))=sockread.recvfrom(100)
					print posicao
					jogada_adv(int(posicao))
					while jogo==True:
						jogadavalida=0
						print "Voce e o simbolo:x"
						desenha_jogo()
						while jogadavalida==0:
							posicao= int(raw_input("E a sua vez de jogar, introduza casa: "))
							jogadavalida=jogada(posicao)
						sockread.sendto("jogar",('127.0.0.1',Server_Port))
						sockread.sendto(str(posicao),('127.0.0.1',Server_Port))
						print " espere pelo seu adversario..."
						(posicao_adv,(ServerIP,ServerPort)) = sockread.recvfrom (100)
						(estado_jogo,(ServerIP,ServerPort)) = sockread.recvfrom (100)
						
						if estado_jogo!="a jogar":
							print estado_jogo
							jogo=False
							sockread.sendto("jogo acabado",('127.0.0.1',Server_Port))
							board= ['1','2','3','4','5','6','7','8','9']
						else:
							jogo=True
						print ("Jogada adversario:"+posicao_adv)
						jogada_adv(int(posicao_adv))
				if answer=="r":
					sockread.sendto("convite rejeitado",('127.0.0.1',Server_Port))
		except Exception, msgs:
			pass

	elif comando in "5":
		termina()
	else:
		print ("Comando nao encontrado")

sockread.close()