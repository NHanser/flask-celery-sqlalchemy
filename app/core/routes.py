from flask import Blueprint,  render_template, redirect, url_for, request
from flask_login import current_user


core_bp = Blueprint('core_bp', __name__, template_folder='templates',
    static_folder='static')


# The Home page is accessible to anyone
@core_bp.route('/')
def home_page():
    if not current_user.is_authenticated:
        return redirect(url_for('security.login', next=request.url))
    return render_template('core/base.html')