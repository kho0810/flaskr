class Config(object):
    SECRET_KEY = "wafjewiofjw;newifu"
    debug = False


class Production(Config):
    debug = True
    CSRF_ENABLED = False
    ADMIN = "kho0810@gmail.com"
    SQLALCHEMY_DATABASE_URI = 'mysql+gaerdbms:///flaskr?instance=hyung-ook:flaskr-instance'
    migration_directory = 'migrations'
