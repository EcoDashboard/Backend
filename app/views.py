from flask import render_template
from app import app
import json
from flask import request, jsonify, session, escape
from app import models, db 
import hashlib

users={'naveen':'password','hanwei':123456}

@app.route('/')
@app.route('/index')
def index():
    if 'email' in session:
        return '{email:%s, login=true}' % escape(session['email'])
    return render_template("index.html")

@app.route('/login', methods=['POST'])
def login():
	email=request.form['email']
	password=request.form['password']
	
	userInDB = models.user_data.query.filter(models.user_data.email == email).filter(models.user_data.password == hashlib.sha256(password).hexdigest()).all()
	
	rs = False
	
	if len(userInDB) == 1:
		rs = True
		session['email'] = request.form['email']
	else:
		rs = False
		
	return str(rs)
        '''return redirect(url_for('index'))
    return render_template("index.html")'''

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
	indicators = models.indicator_def.query.all()
	return  jsonify(json_list=[i.returnString() for i in indicators])
		
#lalalallala
