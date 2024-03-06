from flask import Blueprint, render_template, request,flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .data_operations import get_roles, get_user_by_email, create_user, update_user_password_by_email
from .models import User


auth  = Blueprint('auth', __name__)

def is_valid_password(passwd):
     
  SpecialSym =['$', '@', '#', '%']
  val = True
  if len(passwd) < 8 or not any(char in SpecialSym for char in passwd):
      val = False
  
  return val

def create_new_user(
    email, 
    pwd, 
    pwd1, 
    role_id, 
    first_name, 
    last_name, 
    address, 
    phone, 
    work_phone, 
    department_id, 
    position_id):
  user = get_user_by_email(email)

  try:
    if user:
      flash('Email already exists.', category='error')
    elif pwd != pwd1:
      flash('Passwords don\'t match.', category='error')
    elif not is_valid_password(pwd):
      flash('Password must be at least 8 characters and one of the symbols $@# .', category='error')
    else:
      hashed_pwd = generate_password_hash(pwd)
      create_user(
        email=email,
        password=hashed_pwd,
        role_id=role_id,
        department_id=department_id,
        position_id=position_id,
        first_name=first_name,
        last_name=last_name,
        address=address,
        work_phone=work_phone,
        phone=phone
      )

      flash('Account created!', category='success')
      return True
  except Exception as e:
    flash('Account creation failed: {e}', category='error')
    return False


@auth.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    email = request.form.get('email')
    password = request.form.get('pwd')
    try:
      user_data = get_user_by_email(email)
      if user_data:
        print(user_data["password"])
        stored_password_hash = user_data["password"]

        if check_password_hash(stored_password_hash, password):

          user = User(
            user_id=user_data['id'],
            email=user_data['email'],
            password_hash=user_data['password'],
            state_id=user_data['state_id'],
            role_id=user_data['role_id']
          )        
          login_user(user, remember=True)
          flash('Logged in successfully!', category='success')
          return redirect(url_for('dashboards.dashboard'))
        else:
          flash('Password is incorrect', category='error')
      else:
        flash('Email does not exist.', category='error')
    except Exception as e:
      flash(f'Login failed: {e}', category='error')

  return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'GET':
    roles = get_roles()
    return render_template('register.html', roles=roles)
  if request.method == 'POST':

    email = request.form.get('email')
    pwd = request.form.get('pwd')
    pwd1 = request.form.get('re-pwd')
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    role_id = 3

    try:
      # Create new user
      create_new_user(
          email=email,
          pwd=pwd,
          pwd1=pwd1,
          role_id=role_id,
          first_name=fname,
          last_name=lname,
          address=None,  
          phone=None,
          work_phone=None,
          department_id=None,
          position_id=None,
      )
    
      # Retrieve the newly created user
      user_data = get_user_by_email(email)

      if(user_data) :
        user = User(
          user_id=user_data['id'],
          email=user_data['email'],
          password_hash=user_data['password'],
          state_id=user_data['state_id'],
          role_id=user_data['role_id']
        ) 
        login_user(user, remember=True)
        flash('Account created!', category='success')

        return redirect(url_for('dashboards.dashboard'))
      else:
        flash('Oppos failed.', category='error')
    except Exception as e:
      print(e)
      flash('Account creation failed: {e}', category='error')
      
  return redirect(request.url)


@auth.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
  if request.method == 'POST':
    email = request.form.get('email')
    pwd = request.form.get('pwd')
    pwd1 = request.form.get('re-pwd')

    user_data = get_user_by_email(email)

    if not user_data:
      flash('Email does not exist.', category='error')
    else:
      if pwd != pwd1:
        flash('Passwords don\'t match.', category='error')
      elif not is_valid_password(pwd):
        flash('Password must be at least 8 characters and one of the symbols $@#. ', category='error')
      else:
        hashed_pwd = generate_password_hash(pwd)
        update_user_password_by_email(email, hashed_pwd)
        flash('Password updated!', category='success')
        return redirect(url_for('dashboards.dashboard'))

  return render_template('reset_password.html')
