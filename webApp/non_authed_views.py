from flask import Blueprint, render_template
from webApp import init_db

non_authed_views  = Blueprint('non_authed_views', __name__)

@non_authed_views.route('/')
def home():
  return render_template('home.html')
