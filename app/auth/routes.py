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

@auth_bp.route('/logout/')
@login_required
def logout():
    logout_user()

    return redirect(url_for('auth_bp.index'))


@auth_bp.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated or app.config.get("REGISTRATION_CLOSED") == 1:
        return redirect(url_for('main.home_page'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('auth_bp.loginmyapp'))

    return render_template('register.html', title='Register', form=form)