# -*-coding: utf-8-*-
import SOAPpy
import pika 
from threading import Thread
import time

import sender
import receiver

soap_server = SOAPpy.SOAPServer(('localhost', 8080))

connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))
channel = connection.channel()

# Cria a fila de status dos usuários 
def add_user(user_name):
	sender.conect_user(user_name)
	receiver.conect_user(user_name)

# Atualiza o registro do usuário na fila de usuários
def update_user(user_name, status):
	sender.post_user_status(user_name, status)
	print("server: " + str(user_name))

def get_users(user_name):
	return receiver.list_users(user_name)

def remove_user(user_name):
	channel.queue_delete(queue = user_name) 

def send_message(sender, receiver, msg):

	channel.basic_publish(exchange    = "messages",
						  routing_key = receiver,
						  body        = sender + "#" + msg)

def receive_message(user_name):
	global received_msg
	received_msg = ""

	def callback(ch, method, properties, body):
		global received_msg
		received_msg = body

	channel.basic_consume(callback,      
						  queue  = "msg_" + user_name, 
						  no_ack = True)   
	return received_msg

soap_server.registerFunction(add_user)
soap_server.registerFunction(update_user)
soap_server.registerFunction(get_users)
soap_server.registerFunction(remove_user)
soap_server.registerFunction(send_message)
soap_server.registerFunction(receive_message)

def run_soap_server():
	soap_server.serve_forever()

# Executa o webservice em uma thread, pois o processo é bloqueante
run_server = Thread(target = run_soap_server)
run_server.daemon = True
run_server.start()

while True:
	channel.start_consuming()
