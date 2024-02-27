from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .data_operations import get_employees_by_role,get_pest_controllers, get_user_info_by_user_id,get_departments, get_positions
from .models import User

authed_views  = Blueprint('authed_views', __name__)

# DASHBAORD
@authed_views.route('/dashboard')
@login_required
def dashboard():
  
  current_user_info = get_user_info_by_user_id()
  
  employees = get_employees_by_role(1)
  departments = get_departments()
  positions = get_positions()
  admin = get_employees_by_role(2)
  pest_controllers = get_pest_controllers()
  
  # return render_template(
  #   'dashboard/index.html',
  #   admin_len=3,
  #   employ_len=1,
  #   controller_len=0,
  #   user_info={'id': 2, 'user_id': 2, 'position_id': None, 'department_id': None, 'first_name': 'admin',
  #         'last_name': 'zhang', 'work_phone': None, 'hired_at':'15/02/2024'}
  # )
  
  return render_template(
    'dashboard/index.html',
    admin_len=len(admin),
    employ_len=len(employees),
    controller_len=len(pest_controllers),
    user_info=current_user_info,
    departments=departments,
    positions=positions
  )

@authed_views.route('/manage_staff')
@login_required
def manage_staff():
  employees = get_employees_by_role(1)
  return render_template('dashboard/manage_staff.html', employees=employees)

# PEST
@authed_views.route('/pest')
# @login_required
def pest():
  return render_template('pest/index.html')