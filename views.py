from flask import render_template, redirect, flash, url_for, g
from flask_login import login_user, logout_user, current_user, login_required
from forms import LoginForm
from ref_prj import app, db, login_manager
from models import Usersdb


@app.before_request
def before_request():
    g.user = current_user


@login_manager.user_loader
def load_user(id_user):
    return Usersdb.query.get(int(id_user))


@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('index'))


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html')


@app.route('/login', methods=('GET', 'POST'))
def login():
    if g.user is not None and g.user.is_authenticated:
        flash('Пользователь - {}'.format(g.user))
        redirect(url_for('user', name=g.user))
    form = LoginForm()
    if form.validate_on_submit():
        flash('Пользователь {} добро пожаловать!!!'.format(form.username.data))
        # session['username'] = form.username.data
        login_user(form.username.data)
        return redirect(url_for('user', g.user))
    return render_template('login.html', form=form)


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
