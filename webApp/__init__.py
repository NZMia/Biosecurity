from flask import Flask, g
from dotenv import load_dotenv
from flask_login import LoginManager
import os
from .data_operations import get_user_by_id
from .models import User
from .config import Config, getCurrConn

load_dotenv()

def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = Config.SECRET_KEY
  app.config['MYSQL_HOST'] = Config.MYSQL_HOST
  app.config['MYSQL_USER'] = Config.MYSQL_USER
  app.config['MYSQL_PASSWORD'] = Config.MYSQL_PASSWORD
  app.config['MYSQL_DB'] = Config.MYSQL_DB

  upload_folder = os.path.join(os.path.dirname(__file__), 'static/uploads')
  app.config['UPLOAD'] = upload_folder
  app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
  app.config['ALLOWED_IMAGE_EXTENSIONS'] = ['PNG', 'JPG', 'JPEG', 'GIF']

  getCurrConn()

  from webApp.auth import auth
  from webApp.general_view import general_view
  from webApp.dashboards import dashboards

  app.register_blueprint(auth, url_prefix='/')
  app.register_blueprint(general_view, url_prefix='/')
  app.register_blueprint(dashboards, url_prefix='/')

  login_manager = LoginManager()
  login_manager.login_view = 'auth.login'
  login_manager.init_app(app)

  @login_manager.user_loader
  def load_user(id):


    user_data = get_user_by_id(id)

    if user_data:
        user = User(
          user_id=user_data['id'],
          email=user_data['email'],
          password_hash=user_data['password'],
          state_id=user_data['state_id'],
          role_id=user_data['role_id']
        )

        return user

    return None  # User not found

  return app