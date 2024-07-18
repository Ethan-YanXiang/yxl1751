from app import app
# 從 py檔(模組) 調用 實例
from app.forms1 import LoginForm, RegistrationForm
# 從 包.py檔(模組) 調用 類

from flask import render_template, redirect, url_for, flash  # 一次性 error message
from datetime import datetime
# 從 包 調用 模組


@app.route('/')
@app.route('/index')
def home_func():
    return render_template('index.html')


@app.route('/datetime')
def time_func():
    now = datetime.now()
    return render_template('datetime.html', title='Date & Time', now=now)


@app.route('/login', methods=['GET', 'POST'])  # POST: safely send sensitive data to a server page
def login_func():
    form = LoginForm()  # 呼叫 LoginForm() 類，初始化一個 form object

    userdata = form.username.data
    password_data = form.password.data
    try:
        if userdata.lower() == 'admin':
            flash(f'Username can\'t be {form.username.data}', 'danger')
        elif not userdata.isalpha() and userdata:
            flash(f'Username must be alphanumeric', 'danger')
        elif not password_data.isdigit() and password_data:
            flash(f'Password must be digit', 'danger')
        elif len(password_data) < 4:
            flash(f'Password must be at least 4 characters', 'danger')
        elif form.validate_on_submit():  # all fields validate correctly, request via POST, return True.
            flash(f'Login for {form.username.data}', 'success')  # .data = data typed in
            return redirect(url_for('home_func'))  # once login, where should it go (POST)
    except AttributeError:
        pass

    return render_template('login.html', title='Sign In', form=form)
    # fetching the page first time (GET)


@app.route('/register', methods=['GET', 'POST'])
def register_func():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Registration for {form.username.data} received', 'success')
        return redirect(url_for('home_func'))
    return render_template('registration.html', title='Register', form=form)
