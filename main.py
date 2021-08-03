from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm, LocationSearchForm, HotelSearchForm
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required
from flask_login import logout_user, current_user
from flask_behind_proxy import FlaskBehindProxy
from geocoding import getGeocode, getManyIATA, reverseGeocode
from restrictions import getRestrictions, getAdvisoryDF, getEntryExitDF
from restrictions import getChartUrl, getRiskLevel, getCountryName
from webcam import getWebcam, getWebLink, getTitle
from travel import travel_search, hotel_search, flight_search, parse_attraction_details

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e0f41607df67b2931da80b26f69b3f96'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
proxied = FlaskBehindProxy(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

bcrypt = Bcrypt(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')
  
@app.route("/about")
def about():
    return render_template('about.html')
  
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        user = User(username=form.username.data, email=form.email.data, 
                    password=bcrypt.generate_password_hash(form.password.data).decode('utf-8'))
        try:
            db.session.add(user)
            db.session.commit()
        except exc.IntegrityError:
            flash('User not created: Username or email associated with existing account', 'error')
        else:
            flash(f'Account created for {form.username.data}!', 'success')
        finally:
            return redirect(url_for('login')) # if so - send to login page
    return render_template('register.html', title='Register', form=form)
  

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        my_user = db.session.query(User).filter_by(
            username=form.username.data).first()
        if my_user:
            if bcrypt.check_password_hash(
                    my_user.password, form.password.data):
                flash(f'Succesfully logged in', 'success')
                login_user(my_user, remember=form.remember.data)
                return redirect(url_for('home'))
            else:
                flash('Incorrect password', 'error')
                return redirect(url_for('home'))
        else:
            flash('User does not exist', 'error')
            return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)

@app.route('/search', methods=['GET', 'POST'])
def search():
    search = LocationSearchForm()
    if request.method == 'POST':
        coords = getGeocode(search.data['search'])
        if coords is None:
            return '<div class="content" style="font-size: 20px; text-align: center;" <h1>No results found</h1> </div>'
        return search_results(coords[0], coords[1], coords[2])

    return render_template('search.html', form=search)

@app.route('/results/<lat>&<lng>&<name>')
def search_results(lat, lng, name):
#     if search is None:
#         return '<div class="content" style="font-size: 20px; text-align: center;" <h1>No results found</h1> </div>'
    
    return render_template(
        'results.html',
        name=name, lat=lat, lng=lng)

@app.route('/cam/<lat>&<lng>&<name>')
def show_cam_page(lat, lng, name): 
    coords = [lat, lng]
    decoder = getWebcam(coords)
    titles = getTitle(decoder)
    if not titles:
        return f'<div class="content" style="font-size: 20px; text-align: center; padding: 20px" <h1>No results found for "{name}". Try narrowing search.</h1> </div>'
    return render_template('cam.html', title=titles, cams=getWebLink(decoder))

@app.route('/restrictions/<lat>&<lng>')
def show_restrictions_page(lat, lng):
    coords = [lat,lng]
    covid_info = getRestrictions(coords)
    return render_template(
        'restrictions.html',
        tables=[
            getAdvisoryDF(covid_info).to_html(
                header="true",
                escape=False),
            getEntryExitDF(covid_info).to_html(
                header="true",
                escape=False)],
        charts=getChartUrl(covid_info),
        country=getCountryName(covid_info),
        risk=getRiskLevel(covid_info))

@app.route('/travel/search/<lat>&<lng>', methods=['GET', 'POST'])
def travel_search(lat, lng):
    search = HotelSearchForm()
    if search.validate_on_submit():
#           if request.method == 'POST':
        print(search.data)
        return show_travel_page(lat, lng, search.adults.data,
                                search.rooms.data, search.date.data,
                                search.nights.data, search.minPrice.data,
                                search.maxPrice.data)

    return render_template('travel.html', form=search)

@app.route('/travel/results')
def show_travel_page(lat, lng, adults, rooms, date, nights, minPrice, maxPrice):
    hotel = hotel_search(lat, lng, adults, rooms, date, nights, minPrice, maxPrice)
    hotel['name']
    return render_template ('hotels.html', hotels = hotel)

    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
