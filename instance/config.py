import os

class Config(object):
    #Parent Configuration Class
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class DevelopmentConfig(Config):
    #Configurations for Development
    DEBUG = True

class TestingConfig(Config):
    #Configurations for Testing, with a separate database
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://test_db'
    DEBUG = True

class StagingConfig(Config):
    #Configurations for staging
    DEBUG = True

class ProductionConfig(Config):
    #Configurations for Production
    DEBUG = False
    TESTING = False

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig
}
