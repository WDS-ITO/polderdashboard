from flask import Flask, render_template, request,session,redirect, url_for
from datetime import timedelta
class User:
	def __init__(self,id,username,password):
		self.id = id 
		self.username = username
		self.password = password

	def __repr__(self):
		return f'<User: {self.username}'


users = []

users.append(User(id=1,username='karen', password='nerak'))

app = Flask(__name__)
app.secret_key = 'nerak'
app.permanent_session_life = timedelta(minutes=10)


@app.route('/', methods=['GET','POST'])
def home():
	if request.method == 'POST':
		session.permanent = True
		username = request.form['username']
		password = request.form['password']
		user  = [x for x in users if x.username==username][0]
		if user and user.password==password:
			
			session['user_id'] = user.id
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
		username = users[user_id-1].username
		return render_template("index.html", username=username)
	else:
		return redirect(url_for('home')) 
	return render_template('index.html', username=username)
	

if __name__ == '__main__':
	app.run(debug=True)


