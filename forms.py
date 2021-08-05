from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms import SubmitField, BooleanField  # , SelectField
from wtforms.fields.html5 import DateField
from wtforms_components import DateRange
from wtforms import IntegerField
from wtforms.validators import DataRequired, Length, Email
from wtforms.validators import EqualTo, NumberRange
from datetime import date, timedelta

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
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Register')


class LocationSearchForm(FlaskForm):
    search = StringField('Search for a location:',
                         validators=[DataRequired()])
    submit = SubmitField('Search')


class HotelSearchForm(FlaskForm):
    adults = IntegerField('How many adults will be staying?',
                          validators=[DataRequired(), NumberRange(min=1, max=100)])
    rooms = IntegerField('How many rooms would you like?',
                         validators=[DataRequired(), NumberRange(min=1, max=100)])
    date = DateField('When would you like to check in?',
                     validators=[DataRequired(), DateRange(min=date.today() + timedelta(days=1))], format='%Y-%m-%d')
    nights = IntegerField('How many nights would you like to stay?',
                          validators=[DataRequired(), NumberRange(min=1, max=170)])
    minPrice = IntegerField('Minimum price (per night)',
                            validators=[DataRequired()])
    maxPrice = IntegerField('Please enter your maximum price per night',
                            validators=[DataRequired()])
    submit = SubmitField('Search')


class FlightSearchForm(FlaskForm):
    depart = StringField('Where are you departing from?',
                         validators=[DataRequired()])
    adults = IntegerField('How many adults will be traveling?',
                          validators=[DataRequired(), NumberRange(min=1, max=100)])
    date = DateField('When would you like to depart?',
                     validators=[DataRequired(), DateRange(min=date.today() + timedelta(days=1))], format='%Y-%m-%d')
    submit = SubmitField('Search')
