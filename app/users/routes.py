from flask import Blueprint, render_template, redirect, request, url_for
from flask_security import auth_required 
from flask_login import current_user
from app.extensions import db
from app.users.models import UserProfileForm


users_bp = Blueprint('users_bp', __name__, template_folder='templates',
                    static_folder='static')

@users_bp.route('/profile', methods=['GET', 'POST'])
@auth_required()
def user_profile_page():
    # Initialize form
    form = UserProfileForm(request.form, obj=current_user)

    # Process valid POST
    if request.method == 'POST' and form.validate():
        # Copy form fields to user_profile fields
        form.populate_obj(current_user)

        # Save user_profile
        db.session.commit()

        # Redirect to home page
        return redirect(url_for('core.home_page'))

    # Process GET or invalid POST
    return render_template('users/user_profile_page.html',
                           form=form)