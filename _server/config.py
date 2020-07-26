class Mysql:
    host = "35.225.74.52"
    user = "root"
    password = "livethere2020"
    db = "livethere"


mysql_db_uri = f'mysql+pymysql://{Mysql.user}:{Mysql.password}@{Mysql.host}/{Mysql.db}'

class SqlAlchemyConfig(object):
    SQLALCHEMY_DATABASE_URI = mysql_db_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_HEADERS = 'Content-Type'
