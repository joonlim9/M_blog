from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from market import db
from werkzeug.security import generate_password_hash,check_password_hash
from market.models import User
from market.users.forms import RegisterForm, LoginForm


users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering! Now you can login!')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Logged in successfully.')
            next = request.args.get('next')
            if next == None or not next[0]=='/':
                next = url_for('core.info')
            return redirect(next)
    return render_template('login.html', form=form)

@users.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for('core.info'))