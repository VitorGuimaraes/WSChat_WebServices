#!/usr/bin/env python
# -*-coding: utf-8-*-
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Cria a Exchange
channel.exchange_declare(exchange = 'logs', exchange_type='fanout')

# Cria uma queue de nome aleatorio que é apagada quando o receiver cai
result = channel.queue_declare(exclusive = True)

queue_name = result.method.queue # Pega o nome da queue
print(queue_name)

# Conecta a queue com a exchange
channel.queue_bind(exchange = 'logs',
                   queue    = queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r" % body)

channel.basic_consume(callback,
                      queue  = queue_name,
                      no_ack = True)

channel.start_consuming()