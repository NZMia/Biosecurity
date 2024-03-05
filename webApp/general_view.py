from flask import Blueprint, render_template
from flask_login import login_required
from webApp.data_operations import get_pests, get_pest


general_view  = Blueprint('general_view', __name__)


@general_view.route('/')
def home():
  return render_template('home.html')

# PEST
@general_view.route('/pest')
@login_required
def pest():
  pests = get_pests()
  if pests is None:
    return render_template('error.html', message="Error: No pests found")
  else:
    return render_template('pest/index.html', pests=pests)

  
# PEST DETAIL
@general_view.route('/pest/<int:id>')
@login_required
def pest_detail(id):
  pest = get_pest(id)
  if pest is None:
    print("Error: No pest found")
    # return render_template('error.html', message="Error: No pest found")
  else:
    return render_template('pest/details.html', pest=pest)