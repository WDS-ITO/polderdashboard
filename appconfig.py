from flask import Flask, render_template, request,session,redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_bcrypt import Bcrypt
from ga import ga
from Polder import polder
from datetime import *



app = Flask(__name__)
app.secret_key = 'polder_dashboard'
app.permanent_session_life = timedelta(minutes=10)


app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

app.app_context().push()


if __name__ == '__main__':
	app.run(debug=True)

