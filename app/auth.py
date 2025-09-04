from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.forms import LoginForm, RegistrationForm, UserChangeForm, PasswordChangeForm
from app.models import User
from flask_login import login_user, current_user
from urllib.parse import urlparse, urljoin
from app import db


bp = Blueprint('auth', __name__, url_prefix='/auth')


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile.profile'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login successful!', 'success')

            next_page = request.args.get('next')
            if next_page and is_safe_url(next_page):
                return redirect(next_page)
            return redirect(url_for('profile.profile'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile.profile'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, name=form.name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Registration successful! You are now logged in.', 'success')
        return redirect(url_for('profile.profile'))
    return render_template('register.html', form=form)

@bp.route('/logout', methods=['GET', 'POST'])
def logout(): return 'logout'