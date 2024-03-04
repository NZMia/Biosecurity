import os
from dotenv import load_dotenv

load_dotenv()

class Config():
  CSRF_ENABLED = True

  SECRET_KEY = os.getenv('SECRET', 'get_secret_key')

  MYSQL_HOST = os.getenv('MYSQL_HOST', 'nzmia.mysql.pythonanywhere-services.com')
  MYSQL_USER = os.getenv('MYSQL_USER', 'nzmia')
  MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'admin123#')
  MYSQL_DB = os.getenv('MYSQL_DB', 'nzmia$biosecurity')
