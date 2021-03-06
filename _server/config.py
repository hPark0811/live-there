# User with only read access
class Mysql:
    host = "localhost"
    user = "root"
    password = ""
    db = "livethere"


mysql_db_uri = f'mysql+pymysql://{Mysql.user}:{Mysql.password}@{Mysql.host}/{Mysql.db}'

class SqlAlchemyConfig(object):
    SQLALCHEMY_DATABASE_URI = mysql_db_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_RECYCLE = 300
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_size' : 10, 'pool_recycle' : 300}
    CORS_HEADERS = 'Content-Type'
