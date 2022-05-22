from flask import Blueprint, render_template
from flask_security import auth_required 
from bs4 import BeautifulSoup

dash_bp = Blueprint('dash_bp', __name__, template_folder='templates',
                    static_folder='static')

@dash_bp.route('/dashboard/')
@auth_required()
def dash_page():
    soup = BeautifulSoup('/dashapp', 'html.parser')
    footer = soup.footer
    return render_template('dashapp/dashboard.html', title='Embedded Dash app', footer=footer)