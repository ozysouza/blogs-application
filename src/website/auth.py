from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from src.helpers.log import Log
from src.helpers.forms import RegisterForm, LoginForm
from src.helpers.user_manager import UserManager

# Setup user manager
user_manager = UserManager()

# Setup logging
logger = Log().logger

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET', 'POST'])
def register_user():
    # Ensure login_form is available for all routes.
    login_form = LoginForm()

    register_form = RegisterForm()
    if register_form.validate_on_submit():
        try:
            hashed_password = generate_password_hash(
                register_form.password.data,
                method='pbkdf2:sha256',
                salt_length=8)
            email = register_form.email.data
            first_name = register_form.firstname.data
            last_name = register_form.lastname.data

            if user_manager.get_user_by_email(email):
                flash('Email is already registered.', 'danger')
            else:
                user_manager.add_user(email, first_name, last_name, hashed_password)
                flash('Account created!', 'success')
                return redirect(url_for('auth.register_user'))
        except Exception as err:
            logger.error(f'Error: {err}')
            flash('An error occurred. Please try again.', 'danger')

    return render_template('register.html', register_form=register_form, login_form=login_form)


# TODO: Fix when the user types wrong information the background is changed to an empty page
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Instantiate the login form
    login_form = LoginForm()
    show_modal = False

    if login_form.validate_on_submit():
        # Retrieve user by email and returns a User instance
        user = user_manager.get_user_by_email(login_form.email.data)
        if user:
            if check_password_hash(user.password, login_form.password.data):
                login_user(user, remember=True)
                return redirect(url_for('views.home_page'))
            else:
                flash('Incorrect password. Please try again.', category='danger')
                show_modal = True
        else:
            flash('Email does not exist, please try again.', 'danger')
            show_modal = True
    return render_template('home.html', login_form=login_form, show_modal=show_modal)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('views.home_page'))