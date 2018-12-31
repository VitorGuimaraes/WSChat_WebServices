# -*-coding: utf-8-*-
import SOAPpy
import pika 
from threading import Thread

soap_server = SOAPpy.SOAPServer(('localhost', 8080))