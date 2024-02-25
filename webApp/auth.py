from flask import Blueprint, render_template, request,flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .data_operations import get_roles, get_user_by_email, create_user, create_employee
from webApp import init_db
from .models import User

auth  = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':

    email = request.form.get('email')
    password = request.form.get('pwd')
   
    try:
      user_data = get_user_by_email(email)
      if user_data:
        stored_password_hash = user_data[2]
        if check_password_hash(stored_password_hash, password):
          user = User(*user_data[:-2])          
          login_user(user, remember=True)
          flash('Logged in successfully!', category='success')
          return redirect(url_for('authed_views.dashboard'))
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
  if request.method == 'POST':

    email = request.form.get('email')
    pwd = request.form.get('pwd')
    pwd1 = request.form.get('re-pwd')
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    role_id = request.form.get('role')

    try:
      # cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
      user_data = get_user_by_email(email)

      if user_data:
        flash('Email already exists.', category='error')
      elif pwd != pwd1:
        flash('Passwords don\'t match.', category='error')
      elif len(pwd) < 8:
        flash('Password must be at least 8 characters.', category='error')
      else:

        hashed_pwd = generate_password_hash(pwd)
        
        create_user(email, hashed_pwd, role_id)

        # Retrieve the newly created user
        user = get_user_by_email(email)

        if(user) :
          user_id = user[0]
        
          create_employee(user_id, fname, lname)

          login_user(User(*user[:-2]), remember=True)
          flash('Account created!', category='success')

          return redirect(url_for('authed_views.dashboard'))
        else:
          flash('Account created please login.', category='error')
    except Exception as e:
      print(e)
      flash('Account creation failed: {e}', category='error')
      
  roles = get_roles()
  return render_template('register.html', roles=roles)
