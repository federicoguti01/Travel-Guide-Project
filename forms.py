from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
class LocationSearchForm(FlaskForm):
    search = StringField('Search for a location:',
                        validators=[DataRequired()])
    submit = SubmitField('Search')
    
class HotelSearchForm(FlaskForm):
    adults = IntegerField('How many adults will be staying?',
                        validators=[DataRequired()])
    rooms = IntegerField('How many rooms would you like??',
                        validators=[DataRequired()])
    date = StringField('When would you like to check in? Please enter in the following format: YYYY-MM-DD',
                     validators=[DataRequired()])
    nights = IntegerField('How many nights would you like to stay?',
                          validators=[DataRequired()])
    minPrice = IntegerField('Please enter your minimum price per night',
                            validators=[DataRequired()])
    maxPrice = IntegerField('Please enter your maximum price per night',
														validators=[DataRequired()])
    submit = SubmitField('Search')

    # class FlightSearchForm(FlaskForm):

   #    submit = SubmitField('Search')
  