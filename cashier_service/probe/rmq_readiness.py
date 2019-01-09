""""
 RybbitMQ readiness probe
"""

from pika import ConnectionParameters, BlockingConnection
from os import environ

parameters = ConnectionParameters(environ.get('RABBITMQ_HOST'))
# try to establish connection and check its status
try:
    connection = BlockingConnection(parameters)
    if connection.is_open:
        print('OK')
        connection.close()
        exit(0)
except Exception as error:
    print('Error:', error.__class__.__name__)
    exit(1)
