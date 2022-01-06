import os
import datetime


# Database
DB_ENGINE = 'mysql+pymysql'
DB_SERVER = os.environ.get('DB_SERVER')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_SCHEMA = os.environ.get('DB_SCHEMA')
DB_PORT = os.environ.get('DB_PORT')
DB_CONNECTION_STRING = '{engine}://{user}:{password}@{host}/{schema}'.format(
    engine=DB_ENGINE, user=DB_USER, password=DB_PASS, host=DB_SERVER, port=DB_PORT, schema=DB_SCHEMA)
