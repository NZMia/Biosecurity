from flask import Blueprint, render_template
from webApp import init_db
from flask_login import login_required, current_user

authed_views  = Blueprint('authed_views', __name__)

@authed_views.route('/dashboard')
# @login_required
def dashboard():
  return render_template('dashboard/dashboard.html',user=current_user)

@authed_views.route('/update_profile')
# @login_required
def dashboard():
  return render_template('dashboard/update_profile',user=current_user)