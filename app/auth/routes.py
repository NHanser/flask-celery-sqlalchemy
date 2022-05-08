from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from werkzeug.urls import url_parse
from flask import current_app as app

from app.extensions import db
from app.auth.forms import LoginForm
from app.auth.forms import RegistrationForm
from app.models.user import User

# Blueprint Configuration
auth_bp = Blueprint(
    'auth_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@auth_bp.route('/')
def index():
    return render_template("index.html", title='Home Page')


@auth_bp.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth_bp.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            error = 'Invalid username or password'
            return render_template('login.html', form=form, error=error)

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('auth_bp.index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@auth_bp.route('/logout/')
@login_required
def logout():
    logout_user()

    return redirect(url_for('auth_bp.index'))


@auth_bp.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated or app.config.get("REGISTRATION_CLOSED") == 1:
        return redirect(url_for('auth_bp.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('auth_bp.login'))

    return render_template('register.html', title='Register', form=form)