from flask import Flask, request, redirect, url_for, render_template, session

def create_app():
  app = Flask(__name__)
  app.config['SECRET'] = 'mysecret#123'

  from .views import views
  from .auth import auth

  app.register_blueprint(views, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/auth')

  return app
