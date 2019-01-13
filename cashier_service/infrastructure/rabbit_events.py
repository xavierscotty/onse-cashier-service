from pika import ConnectionParameters, BlockingConnection


class RabbitConnection:
    def __init__(self, config):
        self.queue = config.RABBITMQ_QUEUE
        params = ConnectionParameters(
            host=config.RABBITMQ_HOST,
            heartbeat_interval=int(config.RABBITMQ_HEARTBEAT_INTERVAL),
            blocked_connection_timeout=int(config.RABBITMQ_HEARTBEAT_INTERVAL))
        self._connection = BlockingConnection(params)
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self.queue)

    def get_channel(self):
        return self._connection.channel()


class RabbitBroker(RabbitConnection):
    def __init__(self, config):
        super().__init__(config)

        self.exchange = config.RABBITMQ_EXCHANGE_NAME
        self._channel.exchange_declare(
            self.exchange, exchange_type=config.RABBITMQ_EXCHANGE_TYPE)
        self._channel.queue_bind(queue=self.queue, exchange=self.exchange)
        self._channel.close()

    def produce(self, event):
        """
        Method that will publish messages and handle connections
        """
        channel = self.get_channel()
        channel.basic_publish(exchange=self.exchange,
                              routing_key=self.queue,
                              body=event)
        channel.close()
