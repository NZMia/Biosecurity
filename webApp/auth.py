from flask import Blueprint, render_template, request,flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from webApp import init_db
from flask_login import login_user, login_required, logout_user, current_user
from .models import User

auth  = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    dbConnection = init_db()
    cursor = dbConnection.cursor()

    email = request.form.get('email')
    password = request.form.get('password')
   
    try:
      cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
      user_data = cursor.fetchone()

      if user_data:
        user = User(*user_data)
        if check_password_hash(user.password_hash, password):
          flash('Logged in successfully!', category='success')
          login_user(user, remember=True)
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
    dbConnection = init_db()
    cursor = dbConnection.cursor()

    email = request.form.get('email')
    pwd = request.form.get('pwd')
    pwd1 = request.form.get('re-pwd')

    try:
      cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
      user_data = cursor.fetchone()

      if user_data:
        flash('Email already exists.', category='error')
      elif pwd != pwd1:
        flash('Passwords don\'t match.', category='error')
      elif len(pwd) < 8:
        flash('Password must be at least 8 characters.', category='error')
      else:
        hashed_pwd = generate_password_hash(pwd)
        cursor.execute('INSERT INTO users (email, pwd) VALUES (%s, %s)', (email, hashed_pwd))
        dbConnection.commit()

        flash('Account created!', category='success')
        login_user(User(*user), remember=True)
        return redirect(url_for('authed_view.dashboard'))
      
    except Exception as e:
      flash('Account creation failed: {e}', category='error')
      
  return render_template('register.html')

