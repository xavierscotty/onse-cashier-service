# -*- coding: utf-8 -*-
"""Application configuration."""
from os import environ


class Config(object):
    """Base configuration."""
    # SWAGGER
    SWAGGER_URL = environ.get('SWAGGER_URL', '/docs')
    SWAGGER_FILE_PATH = environ.get('SWAGGER_FILE_PATH', '/swagger.yml')
    # APPLICATION
    APP_NAME = environ.get('APP_NAME', 'Cashier Service API')
    PORT = environ.get('PORT', 5001)


class DevConfig(Config):
    """Development configuration."""
    # RabbitMQ
    RABBITMQ_HOST = environ.get('RABBITMQ_HOST', '')
    RABBITMQ_EXCHANGE_NAME = environ.get('RABBITMQ_EXCHANGE_NAME', '')
    RABBITMQ_EXCHANGE_TYPE = environ.get('RABBITMQ_TYPE', 'fanout')
    RABBITMQ_HEARTBEAT_INTERVAL = environ.get('RABBITMQ_HEARTBEAT_INTERVAL',
                                              600)
    RABBITMQ_CONNECTION_TIMEOUT = environ.get('RABBITMQ_CONNECTION_TIMEOUT',
                                              300)

    @classmethod
    def init_app(cls, app):
        print('THIS APP IS IN DEBUG MODE. \
                YOU SHOULD NOT SEE THIS IN PRODUCTION. ')


class Testing(Config):
    """Testing configuration."""

    @classmethod
    def init_app(cls, app):
        print('THIS APP IS IN DEBUG MODE. \
                YOU SHOULD NOT SEE THIS IN PRODUCTION.')


config = {
    'development': DevConfig,
    'testing': Testing
}
