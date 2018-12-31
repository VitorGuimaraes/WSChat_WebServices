# -*-coding: utf-8-*-
import SOAPpy
import pika 

connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))
channel = connection.channel()

channel.queue_declare(queue="queue")

server = SOAPpy.SOAPProxy("http://localhost:8080/")

# Envio de mensagem para uma queue
channel.basic_publish(exchange    = "",            # Exchange default
					  routing_key = "queue",       # Nome da queue que a mensagem vai
					  body        = "ola mundo")   # Mensagem

channel.basic_publish(exchange    = "",            # Exchange default
					  routing_key = "queue",       # Nome da queue que a mensagem vai
					  body        = "olaa")   # Mensagem

x = server.get_name()
print(x)