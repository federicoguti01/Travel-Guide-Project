from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm, LocationSearch
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required
from flask_login import logout_user, current_user
from flask_behind_proxy import FlaskBehindProxy

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

  
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
  
@app.route("/locations")
def locations():
    form = LocationSearch()
    return render_template('locations.html', form=form)
  
  
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
