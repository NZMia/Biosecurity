from flask import Blueprint, render_template
from flask_login import login_required
from webApp import init_db

general_view  = Blueprint('general_view', __name__)

@general_view.route('/')
def home():
  return render_template('home.html')

# PEST
@general_view.route('/pest')
@login_required
def pest():
  return render_template('pest/index.html')