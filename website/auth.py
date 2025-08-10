from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required  # ✅ IMPORT THESE

from .models import User, db

auth = Blueprint('auth', __name__)

# LOGIN route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    print("ROUTE HIT 🧠")
    print("Request Method:", request.method)

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        print("Email:", email)
        print("Password:", password)

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                login_user(user)  # ✅ LOG THE USER IN
                flash('Logged in successfully ✅', category='success')
                return redirect(url_for('views.home'))  # Make sure 'views.home' exists
            else:
                flash('Incorrect password ❌', category='error')
        else:
            flash('Email not found ❌', category='error')

    return render_template('login.html')


# SIGN-UP route
@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    print("ROUTE HIT 🧠")
    print("Request Method:", request.method)

    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        print("🔥 SIGN-UP FORM SUBMITTED 🔥")

        # Validations
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered 🛑', category='error')
        elif password1 != password2:
            flash('Passwords do not match ❌', category='error')
        elif len(password1) < 6:
            flash('Password too short (min 6 chars) ❌', category='error')
        else:
            hashed_password = generate_password_hash(password1, method='pbkdf2:sha256')
            new_user = User(email=email, first_name=first_name, password=hashed_password)

            db.session.add(new_user)
            db.session.commit()

            flash('Account created successfully 🎉', category='success')
            return redirect(url_for('auth.login'))

    return render_template('sign_up.html')


# LOGOUT route
@auth.route('/logout')
@login_required
def logout():
    logout_user()  # ✅ LOGOUT THE USER
    flash("Logged out successfully 🌙", category='success')
    return redirect(url_for('auth.login'))
