from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, URL, Optional
from models import User

class RegistrationForm(FlaskForm):
    """Form for user registration"""
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        """Check if username is already taken"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken. Please choose a different one.')
    
    def validate_email(self, email):
        """Check if email is already registered"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already registered. Please use a different one.')

class LoginForm(FlaskForm):
    """Form for user login"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class PasswordForm(FlaskForm):
    """Form for adding/editing passwords"""
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    username = StringField('Username/Email', validators=[DataRequired(), Length(max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=255)])
    website = StringField('Website URL', validators=[Optional(), URL(), Length(max=255)])
    category = SelectField('Category', coerce=int)
    notes = TextAreaField('Notes', validators=[Optional(), Length(max=1000)])
    submit = SubmitField('Save')

class CategoryForm(FlaskForm):
    """Form for adding categories"""
    name = StringField('Category Name', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Add Category')

class SearchForm(FlaskForm):
    """Form for searching passwords"""
    query = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')
