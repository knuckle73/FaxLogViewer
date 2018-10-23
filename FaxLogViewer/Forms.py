from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, optional


class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password')
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')


class SearchForm(FlaskForm):
	DateStart = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
	DateEnd = DateField('End Date', format='%Y-%m-%d', validators=[optional()])
	criteria = StringField('Search Criteria')
	LogType = RadioField('Select Record Type', choices=[(1, 'Incoming Faxes'), (2, 'Outgoing Faxes')], default=[1])
	submit = SubmitField('Search')
