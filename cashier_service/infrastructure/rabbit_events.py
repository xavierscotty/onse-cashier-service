from pika import ConnectionParameters, BlockingConnection
from pika.exceptions import AMQPConnectionError


class RabbitBroker:
    def __init__(self, config):
        self._config = config
        self._exchange = config.RABBITMQ_EXCHANGE_NAME

        self._init_connection(config)

    def produce(self, event):
        try:
            self._get_channel().basic_publish(exchange=self._exchange,
                                              routing_key='',
                                              body=event)
        except AMQPConnectionError:
            self._init_connection(self._config)

            self._get_channel().basic_publish(exchange=self._exchange,
                                              routing_key='',
                                              body=event)

    def _init_connection(self, config):
        params = ConnectionParameters(
            host=config.RABBITMQ_HOST,
            heartbeat_interval=int(config.RABBITMQ_HEARTBEAT_INTERVAL),
            blocked_connection_timeout=int(config.RABBITMQ_HEARTBEAT_INTERVAL))

        self._connection = BlockingConnection(params)
        self._channel = self._connection.channel()

        self._channel.exchange_declare(self._exchange, exchange_type='fanout')

    def _get_channel(self):
        return self._connection.channel()
