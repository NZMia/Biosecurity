from flask import Flask, g
from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv()

def init_db():
  if 'db' not in g:
    g.db = mysql.connector.connect(
    host=os.getenv('MYSQL_HOST'),
    user=os.getenv('MYSQL_USER'),
    password=os.getenv('MYSQL_PASSWORD'),
    database=os.getenv('MYSQL_DB')
)
  return g.db

def close_db(e=None):
  db = g.pop('db', None)

  if db is not None:
    db.close()

def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = os.getenv('SECRET')

  from .views import views
  from .auth import auth

  app.register_blueprint(views, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/')

  app.teardown_appcontext(close_db)

  return app
