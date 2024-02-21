from flask import Blueprint, render_template
from webApp import init_db

views  = Blueprint('views', __name__)

@views.route('/')
def home():
  return render_template('home.html')

