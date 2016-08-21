import os
from tinydb import TinyDB

class BaseConfig(object):
    DEBUG = False
    TESTING = False
    DATABASE = TinyDB('db.json')

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
