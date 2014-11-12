from flask import Flask, render_template, session, redirect, url_for, request
from back_end.mongointerface import MongoInterface
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required
import graphlab as gl

app = Flask(__name__)
app.config['SECRET_KEY'] = 'I love to code YOLO'
#called mango on purpose (too many mongo's)
mango = MongoInterface()
model = gl.load_model("model")

@app.route('/', methods=['GET','POST'])
def index():
	'''
	Landing and Login Page
	'''
	return render_template('index.html')

@app.route('/submit_confirmation', methods=['GET','POST'])
def submit_confirmation():
	'''
	Login Checker
	'''
	user_id = request.form['user']
	if mango.login(user_id):
		session['user_id'] = user_id
		return redirect('dashboard')
	else:
		return redirect('/')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
	'''
	Homepage, Root Node
	'''
	category= 'Restaurants'
	user_id = session['user_id']
	sf = model.recommend(users=[user_id], k=300)
	business_list = []
	k = 19
	i = 0
	for bus_id in sf['business_id']:
		bus = mango.get_business(bus_id)
		if category in bus.categories:
			business_list.append(bus)
			if i == k:
				break
			else:
				i += 1

	return render_template('dashboard.html', recommendations=sf, businesses=business_list)

@app.route('/friends', methods=['GET', 'POST'])
def friends():
	return render_template('friends.html')

@app.route('/groups', methods=['GET', 'POST'])
def groups():
	return render_template('groups.html')

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
	return render_template('reviews.html')


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=7777, debug=True)