#!/usr/bin/env python
# -*-coding: utf-8-*-
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Cria a exchange
channel.exchange_declare(exchange = 'logs', exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or "info: Hello World!"

channel.basic_publish(exchange    = 'logs',  # Exchange
                      routing_key = '',      
                      body        = message) # Mensagem

# channel.basic_publish(exchange    = 'logs',  # Exchange
#                       routing_key = '',      
#                       body        = message) # Mensagem

print(" [x] Sent %r" % message)
connection.close()