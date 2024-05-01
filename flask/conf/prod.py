from conf import Config
import os

# testing config
class ProductionConfig(Config):
    def __init__(self):
        self.SQLALCHEMY_DATABASE_URI = get_prod_uri()
        self.DEBUG = bool(os.environ.get("DEBUG"))


    def get_prod_uri(self):
        ## Read secrets
        DB_HOST="mysql"
        DB_NAME="nawas"
        DB_USER="api"
        DB_PASSWORD_FILE="/run/secrets/db_password"
        DB_PASSWORD = None
    
        with open(DB_PASSWORD_FILE) as f:
            DB_PASSWORD = f.readlines()
    
        if DB_PASSWORD is None:
            raise DBPasswordNotFoundException("db_password was not found in the expected location (/run/secrets/db_password)")
    
        return "mysql+mysqlconnector://{}:{}@{}/{}".format(DB_USER,DB_PASSWORD,DB_HOST,DB_NAME)
    
