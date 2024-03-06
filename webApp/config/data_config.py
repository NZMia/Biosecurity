import mysql.connector
from webApp.config import Config

dbconn = None
connection = None

def getCurrConn():
  global dbconn
  global connection

  if dbconn is None:
    dbconn = mysql.connector.connect(
      host=Config.MYSQL_HOST,
      user=Config.MYSQL_USER,
      password=Config.MYSQL_PASSWORD,
      database=Config.MYSQL_DB,
      autocommit=True
    )
    connection = dbconn.cursor(dictionary=True)
  return connection

def closeConnection(cursor):
    dbconn.close()
    connection.close()
