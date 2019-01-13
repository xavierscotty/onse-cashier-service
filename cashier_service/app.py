from flask import Flask
from cashier_service import setup_swagger
from cashier_service.settings import Config
from cashier_service.controllers.health import health
from cashier_service.controllers.process import process


def create(config, broker, logger):
    app = Flask(__name__)
    app.config.from_object(config)
    app.broker = broker
    app.logger = logger

    app.register_blueprint(health)
    app.register_blueprint(process)

    app.register_blueprint(setup_swagger(), url_prefix=Config.SWAGGER_URL)
    return app
