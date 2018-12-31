# -*-coding: utf-8-*-
# System imports:
import time
import string
from threading import Thread

# Third party imports:
import SOAPpy
import pika 
import pygame as pg 
from pygame.locals import *

# Local imports:
from user import User

pg.init()						# Inicializa o pygame
pg.font.init()                  # Inicializa o addon de fontes

SCREEN_SIZE = (402, 715) # Dimensões da tela
BACKGROUND_COLOR = (255, 255, 255)
CAPTION = "WSChat!"

screen = pg.display.set_mode(SCREEN_SIZE)		# Tamanho da janela
screen.fill(BACKGROUND_COLOR)				    # Cor de fundo
pg.display.set_caption(CAPTION)					# Título da janela

# Carregamento de fontes

# Tela de login e envio de mensagem no chat
input_font = pg.font.Font("Fonts/SFProText-Medium.ttf", 17)
# Tela de lista de chats:
chat_list_name = pg.font.Font("Fonts/SFProText-Bold.ttf", 18)
chat_list_info = pg.font.Font("Fonts/SFProText-Regular.ttf", 16)
# Tela de mensagem:
chat_name = pg.font.Font("Fonts/SFProText-Bold.ttf", 16)

# Carregamento de Assets
login_screen   = pg.image.load("assets/login.jpg") 
online         = pg.image.load("assets/online.jpg") 
offline        = pg.image.load("assets/offline.jpg") 
chat_box       = pg.image.load("assets/chat_box.png")
user_cell      = pg.image.load("assets/user_cell.jpg")
online_status  = pg.image.load("assets/online_status.png")
offline_status = pg.image.load("assets/offline_status.png")
chat_window_   = pg.image.load("assets/chat_windows.jpg")

server = SOAPpy.SOAPProxy("http://localhost:8080/")

# Armazena temporariamente os usuários e seus status para exibir na interface
users = []

# Cria um array para mapear as areas de clique na lista de chat
y0 = 120
map_chats_click = []
while y0 <= 665:
    y2 = y0 + 77
    map_chats_click.append((y0, y2))
    y0 = y2 + 1

def cell_data(pos_y):
	for index, position in enumerate(map_chats_click):
		if pos_y >= position[0] and pos_y <= position[1]:
			return index

# Escreve o nome e mensagens no chat
def general_input(event, use_case):
	global current_string
	global text 
	# global chat_queue

	if event.key == K_BACKSPACE:
		current_string = current_string[0:-1] # A tecla backspace apaga uma letra

	elif event.key == pg.K_RETURN and use_case == "send_message":     

		## chat_queue.append(chat)				  # Insere nova mensagem no array do chat
		current_string = []					 	  # Esvazia o buffer da mensagem digitada
		show_chat_window()						  # Atualiza o chat

	elif event.key <= 255:						  # Aceita letras no padrão ASCII
		if len(current_string) < 25:		 	  # Limita a quantidade de caracteres
			current_string.append(chr(event.key)) # Armazena cada tecla digitada para formar a mensagem. Ex: (["o"], ["l"], "[a]")

	text = string.join(current_string, "")		  # Junta as letras digitadas em uma string só. Ex: ("ola")
	
	if use_case == "insert_username":
		screen.blit(login_screen, (0, 0))	      # Redesenha a tela de login
		screen.blit(input_font.render(text, 1, (0, 0, 0)), (46, 212)) # Desenha a palavra digitada

	elif use_case == "send_message":
		screen.blit(chat_box, (0, 0))	          # Redesenha a caixa de texto
		# Corrigir posição
		screen.blit(input_font.render(text, 1, (0, 0, 0)), (0, 680)) # Desenha a palavra digitada

	pg.display.update()							    # Renderiza a tela

def split_user(user_name):
	global users

	name, status = user_name.split("#")

	if len(users) > 0:
		print
		# Se o nome de usuário não existe no array, adiciona o usuário no array
		if name not in [user[0] for user in users]: 
			users.append([name, status])
		
		# Se o nome já existe, apenas atualiza o status desse usuário
		for user in users:
			if user[0] == name: 
				user[1] = status

	else:
		users.append([name, status])

	render_users()

def render_users():
	user_cell_y       = 120
	user_name_photo_y = 132

	for user in users:
		if user[0] != my_username:
			screen.blit(user_cell, (0,  user_cell_y))
			screen.blit(chat_list_name.render(user[0], 1, (0, 0, 0)), (90, user_name_photo_y))
			
			if user[1] == "online":
				screen.blit(online_status, (0,  user_name_photo_y))
			
			elif user[1] == "offline":
				screen.blit(offline_status, (0,  user_name_photo_y))
			
			pg.display.update() 

			user_cell_y       += 77
			user_name_photo_y += 77

def update_contact_list():

	while chat_list: 
		user = server.get_users(my_username)

		split_user(user)
		print(users)
		time.sleep(2)
		
def main():

	global current_string
	global text 
	global my_username 
	global my_status
	global chat_list

	current_string = []
	text = ""
	my_username = ""
	my_status = "online"

	login = False                                   
	chat_list = False
	chat_window = False

	current_chat = None

	screen.blit(login_screen, (0, 0))
	pg.display.update()
	
	while True: 
	###############################################################################
		while not login:
			for event in pg.event.get():
				if event.type == KEYDOWN:
					general_input(event, "insert_username")
					
				elif event.type == pg.MOUSEBUTTONDOWN:
					x, y = pg.mouse.get_pos()

					if x >= 340 and x <= 384 and y >= 38 and y <= 53 and len(text) > 0:
						my_username = text                      # Armazena seu nome
						server.add_user(my_username)            # Solicita ao WebService que crie uma fila para ele 
																# na fila de usuários
						login = True
						chat_list = True 
						current_string = []					 	  # Esvazia o buffer da mensagem digitada
					
		run_contact_list_updater = Thread(target = update_contact_list)
		run_contact_list_updater.daemon = True
		run_contact_list_updater.start()

		###############################################################################
		
		screen.fill(BACKGROUND_COLOR)	# Cor de fundo
		
		while chat_list: 
			
			if my_status == "online":
				screen.blit(online, (0, 0))
			else: 
				screen.blit(offline, (0, 0))
			pg.display.update()
			
			for event in pg.event.get():
				if event.type == pg.MOUSEBUTTONDOWN:
					x, y = pg.mouse.get_pos()
					print(x, y)
					# Altera status
					if x >= 267 and x <= 391 and y >= 77 and y <= 105:
						if my_status == "online":
							my_status = "offline"

						elif my_status == "offline":
							my_status = "online"
					
					# Clique para conversar com um usuário
					elif y >= 120 and y <= 715:
						current_chat = users[cell_data(y)] # retorna um usuário [nome, status]
						chat_list = False
						chat_window = True
						screen.fill(BACKGROUND_COLOR)	

					pg.display.update()

				elif event.type == QUIT: 
					server.remove_user(my_username)

			server.update_user(my_username, my_status)
			
		while chat_window:
			screen.blit(chat_window_, (0, 0))
			screen.blit
			pg.display.update()

			for event in pg.event.get():
				if event.type == KEYDOWN:
					general_input(event, "send_message")
					
				elif event.type == pg.MOUSEBUTTONDOWN:
					x, y = pg.mouse.get_pos()

					if x >= 5 and x <= 34 and y >= 31 and y <= 58 and len(text) > 0:
						chat_window = False
						chat_list   = True

if __name__ == "__main__":
	main()