from flask import Flask, render_template, request,session,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_bcrypt import Bcrypt



app = Flask(__name__)
app.secret_key = 'polder_dashboard'
app.permanent_session_life = timedelta(minutes=10)


app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)

	def __repr__(self):
		return f'<User: {self.username}'



@app.route('/', methods=['GET','POST'])
def home():
	if request.method == 'POST':
		session.permanent = True
		username = request.form['username']
		password = request.form['password']
		userid = 1
		user  = User.query.filter_by(username=username).first()
		if user and bcrypt.check_password_hash(user.password,password):	
			session['user_id'] = userid
			return redirect(url_for('dashboard'))

		return redirect(url_for('home'))
		""" else:
		if 'user_id' in session:
			return redirect(url_for('dashboard'))"""			
	

	return render_template("login.html")


@app.route('/dashboard')
def dashboard():
	if 'user_id' in session:
		user_id = session['user_id']
		username = 'karen'
		return render_template("index.html", username=username)
	else:
		return redirect(url_for('home')) 
	return render_template('index.html', username=username)
	

if __name__ == '__main__':
	app.run(debug=True)


