from flask import render_template, redirect, flash, url_for, g
from flask_login import login_user, logout_user, current_user, login_required
from . import main
from .forms import LoginForm
from ..models import Usersdb
from app import login_manager


@main.before_request
def before_request():
    g.user = current_user


@login_manager.user_loader
def load_user(id_user):
    return Usersdb.query.get(int(id_user))


@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('.index'))


@main.route('/')
@main.route('/index')
@login_required
def index():
    return render_template('index.html')


@main.route('/login', methods=('GET', 'POST'))
def login():
    if g.user is not None and g.user.is_authenticated:
        redirect(url_for('.user', name=g.user))
    form = LoginForm()
    if form.validate_on_submit():
        flash('Пользователь {} добро пожаловать!!!'.format(form.username.data))
        ref_user = Usersdb.query.filter_by(username=form.username.data).first()
        login_user(ref_user)
        return redirect(url_for('.user', name=ref_user.username))
    return render_template('login.html', form=form)


@main.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


