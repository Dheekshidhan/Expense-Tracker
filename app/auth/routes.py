from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from app.auth import auth_bp
from app.models import User
from app.extensions import db


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handles new user account registration."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))  # Redirect if already logged in

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if user already exists
        user_exists = User.query.filter((User.username == username) | (User.email == email)).first()
        if user_exists:
            flash('Username or Email already registered.', 'danger')
            return redirect(url_for('auth.register'))

        # Securely hash the password and save the new user
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password_hash=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user authentication/login."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        # Verify user exists and check password hash
        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=True)
            # If user was trying to access a protected page, redirect them back there
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard.index'))
        else:
            flash('Login unsuccessful. Please check your email and password.', 'danger')

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """Logs out the current user."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))