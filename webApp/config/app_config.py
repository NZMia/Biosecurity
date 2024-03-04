import os
from dotenv import load_dotenv

load_dotenv()

class Config():
  CSRF_ENABLED = True

  SECRET_KEY = os.getenv('SECRET', None)

  MYSQL_HOST = os.getenv('MYSQL_HOST', None)
  MYSQL_USER = os.getenv('MYSQL_USER', None)
  MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', None)
  MYSQL_DB = os.getenv('MYSQL_DB', None)
