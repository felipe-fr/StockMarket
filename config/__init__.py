class Config(object):
    DEBUG = False
    TESTING = False 
    SECRET_KEY = 'fikwhpdciohwcuidehwoihckjwcij'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
   
    
class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True