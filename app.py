from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_bcrypt import Bcrypt
from ga import ga
from Polder import polder
from datetime import *


app = Flask(__name__)
app.secret_key = 'polder_dashboard'
app.permanent_session_life = timedelta(minutes=10)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

app.app_context().push()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f'<User: {self.username} password: {self.password}'


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        session.permanent = True
        username = request.form['username']
        password = request.form['password']
        userid = 1
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = userid
            session['username'] = username
            return redirect(url_for('dashboard'))
        flash('The password is incorrect!')
        return redirect(url_for('home'))

    return render_template("login.html")


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    # Start
    start_date = '2022-07-01'
    end_date = 'today'
    if 'user_id' in session:
        user_id = session['user_id']
        username = session['username']
        if request.method == 'POST':
            start_date = request.form['start_date']
            end_date = request.form['end_date']

            correct_date = date_check(start_date, end_date)
            start_date = correct_date['startdate']
            end_date = correct_date['enddate']
            if correct_date['message'] != '':
                start_date = '2022-07-01'
                end_date = 'today'
                flash(correct_date['message'])

        return render_template("dashboard.html", username=username, terms_dict=ga.get_terms(), analytics_dict=ga.get_analytics_date(start_date, end_date))
    else:
        return redirect(url_for('home'))
    return render_template('dashboard.html', username=username)


@app.route('/search_terms', methods=['GET', 'POST'])
def search_terms():
    start_date = '2022-07-01'
    end_date = 'today'
    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        correct_date = date_check(start_date, end_date)
        start_date = correct_date['startdate']
        end_date = correct_date['enddate']
        if correct_date['message'] != '':
        	start_date = '2022-07-01'
        	end_date = 'today'
        	flash(correct_date['message'])
            

    return render_template('terms.html', terms_dict=ga.get_analytics_date(start_date, end_date), data=ga.get_analytics_date(start_date, end_date)['search_data'])


@app.route('/repositories', methods=['GET', 'POST'])
def repositories():
    start_date = '2022-07-01'
    end_date = 'today'
    total_results = polder.get_total_results()
    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']
    return render_template('repositories.html', total_results=total_results)


@app.route('/analytics', methods=['GET', 'POST'])
def analytics():

    return render_template('analytics.html')


def date_check(startdate, enddate):
    start_date = startdate
    end_date = enddate
    message = ''
    if start_date > end_date:
        message = 'Please enter correct dates'

    elif start_date == '' or end_date == '':
        message = 'Please enter a start date and end date'

    elif start_date < '2022-07-11':
        message = 'please enter a start date after July 11th'

    elif start_date > str(date.today()):
        message = 'You cannot enter a date in the future'

    return {'startdate': start_date,
            'enddate': end_date,
            'message': message}


if __name__ == '__main__':
    app.run(debug=True)
