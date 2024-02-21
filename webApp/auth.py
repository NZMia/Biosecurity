from flask import Blueprint, render_template, request,flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from webApp import init_db

auth  = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    data = request.form
    email = request.form.get('email')
    password = request.form.get('password')
    print(data)
  return render_template('login.html')

@auth.route('/logout')
def logout():
  return "Logout"

@auth.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    dbConnection = init_db()
    cursor = dbConnection.cursor()

    email = request.form.get('email')
    pwd = request.form.get('pwd')
    pwd1 = request.form.get('re-pwd')
    print(pwd)
    try:
      cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
      user = cursor.fetchone()

      if user:
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
        return redirect(url_for('views.home'))
      
    except Exception as e:
      flash('Account creation failed: {e}', category='error')
      
  return render_template('register.html')

