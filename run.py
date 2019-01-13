import structlog

from cashier_service import app
from cashier_service.infrastructure.rabbit_events import RabbitBroker
from cashier_service.settings import config, Config

if __name__ == "__main__":
    broker = RabbitBroker(config['development'])
    app.create(config=config['development'],
               broker=broker,
               logger=structlog.get_logger()
               ).run(
        host='0.0.0.0', port=int(Config.PORT))
