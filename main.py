from flask import Flask, render_template, url_for, flash, redirect
# from forms import RegistrationForm, UserInput, Login
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_behind_proxy import FlaskBehindProxy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e0f41607df67b2931da80b26f69b3f96'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
proxied = FlaskBehindProxy(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

@app.route("/")
def home():
    return render_template('home.html')
  
@app.route("/about")
def about():
    return render_template('about.html')
  
  
    
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

