from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import Email,Length,EqualTo,DataRequired,Regexp

class LoginForm(FlaskForm):
  username = StringField(label='ENTER THE USER ID :',validators=[
    DataRequired(message="User ID is required."),
    Length(min=5, max=30, message="User ID must be between 5 and 30 characters.")])
  password = PasswordField(
    label='ENTER YOUR PASSWORD:',
    validators=[DataRequired(message="Password is required.")])
  submit = SubmitField(label='Login')

class RegisterForm(FlaskForm):
  phone = StringField(label='ENTER YOUR PHONE NUMBER:',
    validators=[DataRequired(message="Phone number is required."),
    Regexp(r'^[0-9]{10}$', message="Phone number must be 10 digits.")])
  email=StringField(label="ENTER YOUR EMAIL: ",validators=[
    DataRequired(message='Email is required'),Email(message='Enter a valid email')])
  username = StringField(label='CREATE YOUR USER NAME :',validators=[
    DataRequired(message="User ID is required."),
    Length(min=5, max=30, message="User ID must be between 5 and 30 characters.")])
  password1= PasswordField(
    label='ENTER YOUR PASSWORD:',
    validators=[DataRequired(message="Password is required.")])
  password2= PasswordField(
    label='CONFIRM YOUR PASSWORD :',
    validators=[DataRequired(message="Confirm the password"),EqualTo('password1',message="Password mismatch")])
  submit = SubmitField(label='Register')
