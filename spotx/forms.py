from spotx import app, db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FloatField, SelectField, DateTimeField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional
from flask_login import current_user

# Login form for user authentication
class loginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=150)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=150)])
    submit = SubmitField('Login')

# Registration form for new users
class register_user(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=150)])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    address = StringField('Address', validators=[DataRequired(), Length(max=150)])
    pincode = StringField('Pincode', validators=[DataRequired(), Length(min=6, max=6)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=150)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

# Form to create a new parking lot
class createLotForm(FlaskForm):
    name = StringField('Lot Name', validators=[DataRequired(), Length(min=2, max=150)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    location = StringField('Location', validators=[DataRequired(), Length(max=150)])
    address = StringField('Address', validators=[DataRequired(), Length(max=150)])
    pincode = StringField('Pincode', validators=[DataRequired(), Length(min=6, max=6)])
    price_per_hour = FloatField('Price per Hour', validators=[DataRequired()])
    no_of_spots = StringField('Number of Spots', validators=[DataRequired()])
    submit = SubmitField('Create Lot')

# Form to book a parking spot
class bookSpotForm(FlaskForm):
    spot_id = IntegerField('Spot ID', render_kw={'readonly': True}, validators=[DataRequired()])
    spot_name = IntegerField('Spot Name', render_kw={'readonly': True}, validators=[DataRequired()])
    lot_id = IntegerField('Lot ID', render_kw={'readonly': True}, validators=[DataRequired()])
    start_time = DateTimeField('Start Time', render_kw={'readonly': True}, validators=[DataRequired()])
    vehicle_number = StringField('Vehicle Number', validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('Book Spot')

# Form to update parking lot details
class UpdateLotForm(FlaskForm):
    name = StringField('Lot Name', validators=[DataRequired(), Length(min=2, max=150)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    location = StringField('Location', validators=[DataRequired(), Length(max=150)])
    price_per_hour = FloatField('Price per Hour',  validators=[DataRequired()])
    address = StringField('ADDRESS', validators=[DataRequired(), Length(max=150)])
    des = TextAreaField('Description', validators=[Length(max=500)])
    pincode = StringField('Pincode', validators=[DataRequired(), Length(min=6, max=6)])
    no_of_spots = StringField('Number of Spots', render_kw={'readonly': True}, validators=[DataRequired()])
    submit = SubmitField('Update Lot')

# Admin search form for users and lots
class searchForm(FlaskForm):
    category = SelectField(
        'Search Category',
        choices=[
            ('username', 'Username'),
            ('email', 'Email'),
            ('user_id', 'User ID'),
            ('lot_id', 'Lot ID'),
            ('pincode', 'Pincode'),
            ('lot_name', 'Lot Name'),
            ('lot_location', 'Location')
        ],
        validators=[DataRequired()]
    )
    search = StringField('Search', validators=[DataRequired(), Length(min=1, max=150)])
    submit = SubmitField('Search')

# User search form for lots
class UserSearchForm(FlaskForm):
    category = SelectField(
        'Search Category',
        choices=[
            ('lot_id', 'Lot ID'),
            ('lot_name', 'Lot Name'),
            ('lot_location', 'Location'),
            ('pincode', 'PIN CODE')
        ],
        validators=[DataRequired()]
    )
    search = StringField('Search', validators=[DataRequired(), Length(min=1, max=150)])
    submit = SubmitField('Search')

# Form to update user details
class UpdateUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=150)])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    address = StringField('Address', validators=[Optional(), Length(max=150)])
    pincode = StringField('Pincode', validators=[Optional(), Length(min=6, max=6)])
    password = PasswordField('Password(OPTIONAL)', validators=[Optional(), Length(min=6, max=150)])
    confirm_password = PasswordField('Confirm Password', validators=[Optional(), EqualTo('password')])
    submit = SubmitField('Update User')

# Form to add more spots to a lot
class AddSpotForm(FlaskForm):
    num_spots = StringField('Number of Spots', validators=[DataRequired()])
    submit = SubmitField('Add Spots')

# Form to end a booking
class end_bookingForm(FlaskForm):
    submit = SubmitField('End Booking')

# Form to release a spot (end booking)
class release_Form(FlaskForm):
    submit = SubmitField('END BOOKING')

# Generic submit form
class submit_Form(FlaskForm):
    submit = SubmitField('Submit')