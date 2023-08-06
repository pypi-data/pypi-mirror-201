import os
import pymssql
RABBITMQ_USERNAME = str(os.environ.get('RABBITMQ_USERNAME'))
RABBITMQ_PASSWORD = str(os.environ.get('RABBITMQ_PASSWORD'))
RABBITMQ_DNS = 'rabbitmq' #os.environ.get('RABBITMQ_DNS')

DB_HOST = 'SQL-WIN-DEV-03\\SQLWINDEV03'
DB_NAME = 'Infradeep'
DB_USER = 'INFRADEEP'
DB_PASSWORD = '1725957f7763b57a4fe450c7b697cc70'

RESULT_FOLDER = "C:/Users/LucienM/source/InfradeepBackV2/csv"

def createConnection():
    """Create a connection to the database"""
    conn = pymssql.connect(
        server=DB_HOST, 
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
        )
    return conn