from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import Flask, flash, render_template, redirect, url_for

from app.factory.database import db
from app.models import User


def verify_login(form):
    user = User.query.filter_by(username=form.username.data).first()
    if user:
        if check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('dashboard'))
    db.session.commit()
    flash("Not valid user")
    return render_template('login.html', form=form)


def create_user(form):
    try:
        hashed_password = generate_password_hash(
            form.password.data, method='sha256')
        new_user = User(username=form.username.data,
                        email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("User created successfully")
        return redirect(url_for('index'))
    except:
        flash("Username or email already being used")
        render_template('signup.html', form=form)
