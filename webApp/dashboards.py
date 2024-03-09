from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_from_directory
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .data_operations import get_employees_by_role,get_customers, get_current_user,get_departments, get_positions, update_employee_by_id, update_user_status_by_id, get_roles, update_customer_by_id,create_pest, get_pests, update_pest_state_by_id, add_pests_image, update_pest_by_id

from .auth import create_new_user

import os

dashboards  = Blueprint('dashboards', __name__)

# Image upload
def image_upload(image):
  if request.files:
    app = current_app 
    filename = secure_filename(image.filename)
    image.save(os.path.join(app.config['UPLOAD'], filename))
    flash('Image uploaded successfully!', category='success')
    return send_from_directory(app.config['UPLOAD'], filename)
  else:
    flash('No image selected', category='error')
    return False

# Admin dashboard (get Admin, update admin)
@dashboards.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
  if request.method == 'GET':
    current_user_info = get_current_user()
    departments = get_departments()
    positions = get_positions()
    return render_template(
      'dashboard/index.html',
      user_info=current_user_info,
      departments=departments,
      positions=positions
    )
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
      return redirect(request.url)
    except Exception as e:
      flash(f'Employee update failed: {e}', category='error')

  return redirect(request.url)

# Staff dashboard( get staff, update staff, delete staff, add staff)
@dashboards.route('/manage_staff', methods=['GET', 'POST'] )
@login_required
def manage_staff():
    departments = get_departments()
    roles = get_roles()
    positions = get_positions()

    if request.method == 'GET':
        employees = get_employees_by_role(1)
        return render_template(
            'dashboard/manage_staff.html',
            employees=employees,
            departments=departments,
            positions=positions,
            roles=roles
        )

    if request.method == 'POST':
        data = request.form

        if 'delete_form' in request.form:
            try:
                id = data.get('user_id')
                update_user_status_by_id(id, 'inactive')
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
                role_id = data.get('role')
                update_employee_by_id(
                    id,
                    first_name=first_name,
                    last_name=last_name,
                    department_id=department_id,
                    position_id=position_id,
                    work_phone=work_phone,
                    role_id=role_id
                )
                flash('User updated successfully!', category='success')
            except Exception as e:
                flash(f'User update failed: {e}', category='error')

        else:
            try:
                email = data.get('email')
                pwd = data.get('pwd')
                pwd1 = data.get('re-pwd')
                fname = data.get('fname')
                lname = data.get('lname')
                position_id = data.get('position_id')
                department_id = data.get('department_id')
                work_phone = data.get('wphone')
                role_id = data.get('role_id')

                is_created = create_new_user(
                    email=email,
                    pwd=pwd,
                    pwd1=pwd1,
                    role_id=role_id,
                    first_name=fname,
                    last_name=lname,
                    address=None,  
                    phone=None,  
                    work_phone=work_phone,  
                    department_id=department_id,  
                    position_id=position_id  
                )

                if is_created:
                    flash('Employee created successfully!', category='success')
                else:
                    flash('Employee creation failed', category='error')

            except Exception as e:
                flash(f'Employee creation failed: {e}', category='error')

    return redirect(request.url)

# Pest controller dashboard (get customer, update customer, delete customer, add customer)
@dashboards.route('/manage_customer', methods=['GET', 'POST'])
@login_required
def manage_customer():
  role = get_roles()
  if request.method == 'GET':
    users = get_customers()
    return render_template('dashboard/manage_customer.html', users=users, roles=role)
  
  if request.method == 'POST':
    data = request.form
    if 'delete_form' in request.form:
      try: 
        id = data.get('user_id')
        update_user_status_by_id(id, 'inactive')
        flash(f'User deleted successfully! {id}', category='success')
      except Exception as e:
        flash(f'User deletion failed: {e}', category='error')

    elif 'update_form' in request.form:
      try:
        id = data.get('user_id')
        first_name = data.get('fname')
        last_name = data.get('lname')
        address = data.get('address')
        phone = data.get('phone')
        role_id=data.get('role_id')
        update_customer_by_id(
          id,
          first_name=first_name,
          last_name=last_name,
          address=address,
          phone=phone,
          role_id=role_id
        )
        
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
        address = data.get('address')
        phone = data.get('phone')
        role_id=data.get('role_id')

        is_crated = create_new_user(
            email=email,
            pwd=pwd,
            pwd1=pwd1,
            role_id=role_id,
            first_name=fname,
            last_name=lname,
            address=address,  
            phone=phone,  
            work_phone=None,  
            department_id=None,  
            position_id=None,  
        )
        if is_crated:
          flash('Employee created successfully!', category='success')
          # role = get_roles()
          users = get_customers()
          print(users)
          return render_template('dashboard/manage_customer.html', users=users, roles=role)
        else:
          flash('Employee creation failed', category='error')
      except Exception as e:
        flash(f'Employee creation failed: {e}', category='error')

  return redirect(request.url)

@dashboards.route('/manage_pest', methods=['GET', 'POST'])
@login_required
def manage_pest():
  if request.method == 'GET':
    pests = get_pests()
    print(pests)
    return render_template('dashboard/manage_pest.html', pests=pests)
  
  if request.method == 'POST':
    data = request.form

    # Delete pest: make it inactive
    if 'delete_form' in request.form:
      try: 
        id = data.get('pest_id')
        update_pest_state_by_id(id, 'inactive')
        flash(f'Pest deleted successfully! {id}', category='success')
      except Exception as e:
        flash(f'Pest deletion failed: {e}', category='error')

    # Add more pest image
    elif 'add_image' in request.form:
      try:
        id = data.get('pest_id')
        img = request.files.get('customFile')
        if img:
          uploaded_image = image_upload(img)
          if uploaded_image:
            add_pests_image(id, img.filename)
            flash('Image added successfully!', category='success')
          else:
            flash('Image upload failed', category='error')
        else:
          flash('No image selected', category='error')
      except Exception as e:
        flash(f'Image upload failed: {e}', category='error')

    #  Update pest
    elif 'update_form' in request.form:
      try:
        id = data.get('pest_id')
        common_name = data.get('common_name')
        scientific_name = data.get('scientific_name')
        img_id = data.get('img_id')
        description = data.get('description')
        distinctive_features = data.get('distinctive_features')
        size = data.get('size')
        droppings = data.get('droppings')
        footprints = data.get('footprints')
        distribution = data.get('distribution')
        impacts = data.get('impacts')
        control_methods = data.get('control_methods')
        
        update_pest_by_id(
          id,
          common_name=common_name,
          scientific_name=scientific_name,
          img_id=img_id,
          description=description,
          distinctive_features=distinctive_features,
          size=size,
          droppings=droppings,
          footprints=footprints,
          distribution=distribution,
          impacts=impacts,
          control_methods=control_methods
        )
        flash('Pest updated successfully!', category='success')
      except Exception as e:
        flash(f'Pest update failed: {e}', category='error')

    # Add pest
    else:
      common_name = data.get('commonName')
      scientific_name = data.get('scientificName')
      description = data.get('description')
      distinctive_features = data.get('distinctiveFeatures')
      size = data.get('size')
      droppings = data.get('droppings')
      footprints = data.get('footprints')
      distribution = data.get('distribution')
      impacts = data.get('impacts')
      control_methods = data.get('controlMethods')

      img = request.files.get('customFile')  # Using get to avoid KeyError
      if img:
        uploaded_image = image_upload(img)
        if uploaded_image:
          try:
            create_pest(
                common_name=common_name,
                scientific_name=scientific_name,
                description=description,
                distinctive_features=distinctive_features,
                size=size,
                droppings=droppings,
                footprints=footprints,
                distribution=distribution,
                impacts=impacts,
                control_methods=control_methods,
                image=img.filename
            )
            flash('Pest created successfully!', category='success')
          except Exception as e:
              flash(f'Pest creation failed: {e}', category='error')
        else:
          flash('Image upload failed', category='error')
      else:
        flash('No image selected', category='error')
  
  return redirect(request.url)
