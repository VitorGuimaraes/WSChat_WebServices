# -*-coding: utf-8-*-
from threading import Thread
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host = "localhost"))
channel = connection.channel()

# Exchange para status dos usuários
channel.exchange_declare(exchange = "users", exchange_type = "fanout")

# Exchange para direcionar mensagens
channel.exchange_declare(exchange = "messages", exchange_type = "direct")

def conect_user(user_name):
	# Cria uma queue de nome aleatorio que é apagada quando o receiver desconecta
	# Usada para registrar o status dos usuários
	channel.queue_declare(queue = "status_" + user_name)

	# Conecta a queue com a exchange de status dos usuários
	channel.queue_bind(exchange = "users",
					   queue    = "status_" + user_name)

	################################################################################

	# Cria uma queue que é apagada quando o receiver desconecta
	# Usada para redirecionar as mensagens dos usuários
	channel.queue_declare(queue = "msg_" + user_name)

	# Conecta a queue com a exchange de status dos usuários
	channel.queue_bind(exchange    = "messages",
					   queue       = "msg_" + user_name,
					   routing_key = user_name)

def list_users(user_name):
	global users_status
	users_status = ""

	def callback(ch, method, properties, body):
		global users_status
		users_status = str(body)
		print("body: %r" % body)
		channel.stop_consuming()

	channel.basic_consume(callback,
						  queue  = "status_" + user_name,
						  no_ack = True)  
	
	channel.start_consuming()

	return users_status