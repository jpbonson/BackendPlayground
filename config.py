import os
import logging
from flask.ext.cache import Cache 
from tinydb import TinyDB

class BaseConfig(object):
    DEBUG = False
    TESTING = False
    DATABASE = TinyDB('db.json')
    CACHE_TYPE = 'simple'
    LOGGING_LOCATION = 'debug.log'
    LOGGING_LEVEL = logging.DEBUG

class ProductionConfig(BaseConfig):
    DATABASE = TinyDB('prod_db.json')

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class TestingConfig(BaseConfig):
    TESTING = True
    DATABASE = TinyDB('tests/db_test.json')

config = {
    "production": "config.ProductionConfig",
    "development": "config.DevelopmentConfig",
    "testing": "config.TestingConfig",
    "default": "config.DevelopmentConfig"
}

def configure_app(app, config_name = os.getenv('FLASK_CONFIGURATION', 'default')):
    app.config.from_object(config[config_name])
    app.cache = Cache(app)
    logging.basicConfig(filename=app.config['LOGGING_LOCATION'],level=app.config['LOGGING_LEVEL'])