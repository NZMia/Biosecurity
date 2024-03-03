from flask import Flask, g
from dotenv import load_dotenv
from flask_login import LoginManager
import os
from webApp.config import Config
from webApp.data_operations import get_user_by_id
from webApp.models import User

load_dotenv()

def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = Config.SECRET_KEY
  upload_folder = os.path.join(os.path.dirname(__file__), 'static/uploads')
  app.config['UPLOAD'] = upload_folder
  app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
  app.config['ALLOWED_IMAGE_EXTENSIONS'] = ['PNG', 'JPG', 'JPEG', 'GIF']

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
          state=user_data['state_id'],
          role_id=user_data['role_id']
        ) 
        
        return user

    return None  # User not found
  
  return app
