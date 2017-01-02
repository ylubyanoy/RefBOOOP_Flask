from flask import Flask, render_template, redirect, flash, url_for, g
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_sqlalchemy import SQLAlchemy
import config
from forms import LoginForm


app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)

db = SQLAlchemy(app)

Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class Usersdb(db.Model):
    # __tablename__ = 'users'

    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200))
    userpass = db.Column(db.String(50))
    isadmin = db.Column(db.Integer)
    otraslid = db.Column(db.Integer)
    isbooop = db.Column(db.Integer)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id_user)

    def __repr__(self):
        return '<User {}>'.format(self.username)


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
        ref_user = Usersdb.query.filter_by(username=form.username.data).first()
        login_user(ref_user)
        return redirect(url_for('user', name=ref_user.username))
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

if __name__ == '__main__':
    app.run()
