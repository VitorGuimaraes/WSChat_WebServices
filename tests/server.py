# -*-coding: utf-8-*-
import SOAPpy
import pika 
from threading import Thread

connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))
channel = connection.channel()
channel.queue_declare(queue = "queue")

def get_name():
	global msg
	msg = ""

	def callback(ch, method, properties, body):
		global msg
		msg = body

	# Consome uma queue
	channel.basic_consume(callback,      
						queue = "queue", 
						no_ack = True)   

	# channel.start_consuming()

	return msg

server = SOAPpy.SOAPServer(("localhost", 8080))
server.registerFunction(get_name)

def run_soap_server():
	while True:
		server.serve_forever()

run_soap = Thread(target = run_soap_server)	  
run_soap.daemon = True					 
run_soap.start()

while True:
	channel.start_consuming()