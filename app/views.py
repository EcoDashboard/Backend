from flask import render_template
from app import app
import json
from flask import request, jsonify
from app import models, db
import hashlib

users={'naveen':'password','hanwei':123456}
@app.route('/')
@app.route('/index')
def index():
	return render_template("index.html")

@app.route('/login', methods=['POST'])

def login():
	
	user=request.form['user_name']
	password=request.form['password']
	if user in users:
		if password ==users.get(user):
			return json.dumps({"naveen":"wazza","hanwei":"hello"})
		else:
			return render_template("index.html",title ='LOGIN PAGE')
	else:
		return "Username or password wrong"

@app.route('/register', methods=['POST'])

def register():
	return render_template("register.html")

@app.route('/saveDetails', methods=['POST'])

def saveDetails():
	user_name=request.form['user_name']
	password=request.form['password']
	hash = hashlib.sha256(password).hexdigest()
	city_id_admin = request.form['city_id_admin']
	email=request.form['email']

	u = models.user_data(user_name=user_name, password=hash, city_id_admin=city_id_admin, email=email)	
	db.session.add(u)
	db.session.commit()	
	db.session.close()

	return user_name

@app.route('/indicatorList', methods=['GET'])
def indicatorList():
	#indicators = models.indicator_def.query.get('1')
	#return  jsonify(indicators.returnString())
	Indicators = db.session.query(models.showIndicators)
	Air_ind = Indicators.filter(models.showIndicators.cat_id == 1)
	Water_ind = Indicators.filter(models.showIndicators.cat_id == 2)
	Land_ind = Indicators.filter(models.showIndicators.cat_id == 3)
	Energy_ind = Indicators.filter(models.showIndicators.cat_id == 4)
	Bio_Diversity_ind = Indicators.filter(models.showIndicators.cat_id == 5)
	return  jsonify( Air = [i.returnString() for i in Air_ind],
			 Water = [i.returnString() for i in Water_ind],
			 Land = [i.returnString() for i in Land_ind],
			 Energy = [i.returnString() for i in Energy_ind],
			 Bio_Diversity = [i.returnString() for i in Bio_Diversity_ind])
