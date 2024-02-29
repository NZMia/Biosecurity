from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .data_operations import get_employees_by_role,get_pest_controllers, get_user_info_by_user_id,get_departments, get_positions, update_employee_by_id, update_user_status_by_id, get_roles, get_user_by_email
from .models import User
from .auth import create_new_user

dashboards  = Blueprint('dashboards', __name__)

@dashboards.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
  # update user info
  if request.method == 'POST':
    data = request.form
    employee_id = current_user.id
    try:
      first_name = data.get('fname')
      last_name = data.get('lname')
      department_id = data.get('department')
      position_id = data.get('position')
      work_phone = data.get('wphone')
      role=data.get('role')
      update_employee_by_id(employee_id, 
                            first_name=first_name, 
                            last_name=last_name, 
                            department_id=department_id, 
                            position_id = position_id,
                            work_phone=work_phone,
                            role=role
                          )
      flash('Employee updated successfully!', category='success')
    except Exception as e:
      flash(f'Employee update failed: {e}', category='error')

  current_user_info = get_user_info_by_user_id()
  
  employees = get_employees_by_role(1)
  departments = get_departments()
  positions = get_positions()
  admin = get_employees_by_role(2)
  pest_controllers = get_pest_controllers()
  return render_template(
    'dashboard/index.html',
    admin_len=len(admin),
    employ_len=len(employees),
    controller_len=len(pest_controllers),
    user_info=current_user_info,
    departments=departments,
    positions=positions
  )

@dashboards.route('/manage_staff', methods=['GET', 'POST'] )
@login_required
def manage_staff():
  departments = get_departments()
  role = get_roles()
  positions = get_positions()
  if request.method == 'POST':
    data = request.form
    if 'delete_form' in request.form:
      try: 
        id = data.get('user_id')
        update_user_status_by_id(id, 'INACTIVE')
        flash(f'User deleted successfully! {id}', category='success')
      except Exception as e:
        flash(f'User deletion failed: {e}', category='error')

    elif 'update_form' in request.form:
      try:
        id = data.get('user_id')
        first_name = data.get('fname')
        last_name = data.get('lname')
        department_id = data.get('department')
        position_id = data.get('position')
        work_phone = data.get('wphone')
        role=data.get('role')
        update_employee_by_id(id, 
          first_name=first_name, 
          last_name=last_name, 
          department_id=department_id, 
          position_id = position_id,
          work_phone=work_phone,
          role=role
        )
        # updated success show success message otherwise show error message
        flash('User updated successfully!', category='success')
      except Exception as e:
        flash(f'User update failed: {e}', category='error')
    else:
      # add user
      try:
        email = data.get('email')
        pwd = data.get('pwd')
        pwd1 = data.get('re-pwd')
        fname = data.get('fname')
        lname = data.get('lname')
        position_id = data.get('position_id')
        department_id = data.get('department_id')
        work_phone = data.get('wphone')
        role_id=data.get('role_id')

        is_crated = create_new_user(
            email=email,
            pwd=pwd,
            pwd1=pwd1,
            role_id=role_id,
            first_name=fname,
            last_name=lname,
            address=None,  # Set default or adjust as needed
            phone=None,  # Set default or adjust as needed
            work_phone=work_phone,  # Set default or adjust as needed
            department_id=department_id,  # Set default or adjust as needed
            position_id=position_id,  # Set default or adjust as needed
        )
        if is_crated:
          flash('Employee created successfully!', category='success')
        else:
          flash('Employee creation failed', category='error')
      except Exception as e:
        flash(f'Employee creation failed: {e}', category='error')

  employees = get_employees_by_role(1)

  return render_template(
    'dashboard/manage_staff.html', 
    employees=employees,
    departments=departments,
    positions=positions,
    roles=role
  )

# PEST
@dashboards.route('/pest')
@login_required
def pest():
  return render_template('pest/index.html')