from flask import Blueprint, render_template
from webApp import init_db
from flask_login import login_required, current_user
non_authed_views  = Blueprint('non_authed_views', __name__)

@non_authed_views.route('/')
def home():
  return render_template('home.html')
