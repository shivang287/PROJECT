"""Authentication routes."""

from flask import Blueprint, render_template, request, redirect, url_for, session,flash

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')



USER_DETAIL = {
    'username' : 'shivang',
    'password' : '1234'
}

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
       username = request.form.get('username')
       password = request.form.get('password')
       if username == USER_DETAIL['username'] and password == USER_DETAIL['password']:
           session['user'] = username
           flash('login successful', 'success')
           return redirect(url_for('tasks.view_tasks'))
       else:
           flash('invailid username or password', 'danger')
    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        # Handle registration logic
        pass
    return render_template('register.html')


@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully', 'info')
    return redirect(url_for('auth.login'))
