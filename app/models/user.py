# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from app.extensions import db
from flask_security import UserMixin, RoleMixin
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from app.extensions import login


@login.user_loader
def load_user(id_):
    return User.query.get(int(id_))


# Define the User data model. Make sure to add the flask_user.UserMixin !!
class User(db.Model, UserMixin):
    __tablename__ = 'user' 
    id = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(255), unique=True) 
    username = db.Column(db.String(255)) 
    password = db.Column(db.String(255)) 
    last_login_at = db.Column(db.DateTime()) 
    current_login_at = db.Column(db.DateTime()) 
    last_login_ip = db.Column(db.String(100)) 
    current_login_ip = db.Column(db.String(100)) 
    login_count = db.Column(db.Integer) 
    active = db.Column(db.Boolean()) 
    confirmed_at = db.Column(db.DateTime()) 
    roles = db.relationship('Role', secondary='roles_users', backref=db.backref('users', lazy='dynamic'))

    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    
    # User information
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
    first_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')
    last_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')

    def has_role(self, role):
        return role in self.roles




# Define the Role data model
class Role(db.Model, RoleMixin):
    __tablename__ = 'role' 
    id = db.Column(db.Integer(), primary_key=True) 
    name = db.Column(db.String(80), unique=True) 
    description = db.Column(db.String(255))
    permissions = db.Column(db.Unicode())
    

# Define the UserRoles association model
class RolesUsers(db.Model):
    __tablename__ = 'roles_users' 
    id = db.Column(db.Integer(), primary_key=True) 
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE')) 
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))


# # Define the User registration form
# # It augments the Flask-User RegisterForm with additional fields
# class MyRegisterForm(RegisterForm):
#     first_name = StringField('First name', validators=[
#         validators.DataRequired('First name is required')])
#     last_name = StringField('Last name', validators=[
#         validators.DataRequired('Last name is required')])


# Define the User profile form
class UserProfileForm(FlaskForm):
    first_name = StringField('First name', validators=[
        validators.DataRequired('First name is required')])
    last_name = StringField('Last name', validators=[
        validators.DataRequired('Last name is required')])
    submit = SubmitField('Save')
