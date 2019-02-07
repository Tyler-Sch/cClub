import os


class BaseConfig:
    TESTING = False

class DevelopmentConfig(BaseConfig):
    DATABASE_URI = os.environ.get('DATABASE_URL')

class TestingConfig(BaseConfig):
    DATABASE_URI = os.environ.get('DATABASE_TEST_URL')
    TESTING = True

class ProductionConfig(BaseConfig):
    DATABASE_URI = os.environ.get('DATABASE_URL')
