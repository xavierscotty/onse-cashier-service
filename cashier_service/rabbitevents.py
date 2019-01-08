from pika import ConnectionParameters, BlockingConnection


class RabbitConnection:
    def __init__(self, properties):
        self.queue = properties['queue']
        params = ConnectionParameters(host=properties['host'],  blocked_connection_timeout=300)
        self.connection = BlockingConnection(params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)


class RabbitProducer(RabbitConnection):
    def __init__(self, properties):
        super().__init__(properties)

        self.exchange = properties['exchange']
        self.channel.exchange_declare(self.exchange, exchange_type='topic')
        self.channel.queue_bind(queue=self.queue, exchange=self.exchange)

    def publish(self, event):
        self.channel.basic_publish(exchange=self.exchange,
                                   routing_key=self.queue,
                                   body=event)
        self.connection.close()
