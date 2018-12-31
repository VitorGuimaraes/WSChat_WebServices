# -*-coding: utf-8-*-
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

def post_user_status(user_name, status):
	channel.basic_publish(exchange      = "users",
						  routing_key   = "",
						  body          = user_name + "#" + status)
