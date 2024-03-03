from flask import Flask, g
from dotenv import load_dotenv
from flask_login import LoginManager
import os
import mysql.connector
from .models import User

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
  upload_folder = os.path.join(os.path.dirname(__file__), 'static/uploads')
  app.config['UPLOAD'] = upload_folder
  app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
  app.config['ALLOWED_IMAGE_EXTENSIONS'] = ['PNG', 'JPG', 'JPEG', 'GIF']

  from .auth import auth
  from .general_view import general_view
  from .dashboards import dashboards

  app.register_blueprint(auth, url_prefix='/')
  app.register_blueprint(general_view, url_prefix='/')
  app.register_blueprint(dashboards, url_prefix='/')

  login_manager = LoginManager()
  login_manager.login_view = 'auth.login'
  login_manager.init_app(app)

  @login_manager.user_loader
  def load_user(id):
      dbConnection = init_db()
      cursor = dbConnection.cursor(dictionary=True)  # Use dictionary cursor for easier access

      cursor.execute('SELECT * FROM users WHERE id = %s', (id,))
      user_data = cursor.fetchone()

      if user_data:
          user = User(
            user_id=user_data['id'],
            email=user_data['email'],
            password_hash=user_data['password'],
            state=user_data['state_id'],
            role_id=user_data['role_id']
          ) 
          
          return user

      return None  # User not found
  
  app.teardown_appcontext(close_db)

  return app
