# config.py


class Config(object):
    """
    Common configurations
    """

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMPLATES_AUTO_RELOAD = True
    UPLOAD_FOLDER = '/home/alisson/www/projects/charts/uploads'
    UPLOADS_DEFAULT_DEST = 'uploads'
    UPLOADS_DEFAULT_URL = "http://192.168.104.37:5000/uploads"


class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    SQLALCHEMY_ECHO = False
    USE_RELOADER = False
    WTF_I18n_ENABLED = True


class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
    }
