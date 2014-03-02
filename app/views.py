from app import app
from app import models, db
from flask import render_template
from flask import request, jsonify, session, escape, Response, g, make_response
from flask.ext.cors import cross_origin
from flask.ext.httpauth import HTTPBasicAuth
from sqlalchemy import func
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import hashlib
import json
import urllib
import re

auth = HTTPBasicAuth()


def generate_auth_token(expiration = 600):
	s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
	return s.dumps({ 'id': g.user.user_id })

def verify_auth_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except:
        return None # valid token, but expired
    user = models.user_data.query.filter(models.user_data.user_id == data['id']).all()
    return user[0]

@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = verify_auth_token(username_or_token)
    if not user:

        # try to authenticate with username/password
        user = models.user_data.query.filter(models.user_data.user_name == username_or_token).first()

        user2 = models.user_data.query.filter(\
        		models.user_data.password == hashlib.sha256(password).hexdigest()\
        		).all()

        if not user or len(user2) != 1:
            return False
    g.user = user if user else user2
    return True

@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = generate_auth_token()
    return jsonify({ 'token': token.decode('ascii') })

@app.route('/')
def default():
	return ''

@app.route('/login_test.html', methods=['GET'])
def index():
    return render_template("index.html")



@app.route('/login', methods=['POST'])
def loginPost():
	print 'HELLO2'
	print request.form
	email=urllib.unquote(request.form['email'])
	password=request.form['password']

	user = models.user_data.query.filter(models.user_data.email == email)\
		.filter(models.user_data.password == hashlib.sha256(password).hexdigest())\
		.first()

	print user

	if user:
		g.user = user
		token = generate_auth_token()
		return jsonify({'token':token})
	else:
		return make_response("",503)


@app.route('/logout', methods=['GET'])
def logout():
	if 'email' in session:
		session.pop('email', None)
		return 'true'

@app.route('/register_test.html')
def registerTest():
	return render_template("register_test.html")


@app.route('/checkCityIdExists')
def checkCityIdExists():
	city_id = request.values.get("city_id");
	return str(checkCityIdExists(city_id))
		

def checkCityIdExists(city_id):
	if not city_id:
		return True
	elif models.city_profile_data.query.filter(models.city_profile_data.city_id == city_id).first():
		return True
	else:
		return False
	

@app.route('/register', methods=['POST'])
@cross_origin()
def register():

	# user
	email = urllib.unquote(request.form['email'].strip()).lower()
	password=request.form['password']
	hash = hashlib.sha256(password).hexdigest()
	contact_firstname = request.form['contact_firstname'].strip()
	contact_lastname = request.form['contact_lastname'].strip()
		
	# city
	city_id = request.form['city_abbre'].strip().upper()
	city_name = request.form['city_name'].strip()
	council_name = request.form['council_name'].strip()
	state = request.form['state'].strip()
	country = request.form['country'].strip()
	postcode = request.form['postcode'].strip()
	area = request.form['area'].strip()
	population = request.form['population'].strip()
	contact_email = request.form['contact_email'].strip()
	contact_number = request.form['contact_number'].strip()
	council_address = request.form['council_address'].strip()

	# check
	errors=[]
	if not email:
		errors.append('Email is empty.')
	elif  models.user_data.query.filter(models.user_data.email == email).first():
		errors.append('Email has already been used.')
	
	if not city_id:
		errors.append('City abbreviation is empty.')
	elif checkCityIdExists(city_id):
		errors.append('City Alias has already been used.')

	if not re.match("^[0-9]*[.]?[0-9]+$", area):
		errors.append('Area format is incorrect.')

	# invalid input
	if errors:
		return Response(json.dumps(errors), mimetype='application/json')

	#insert new city
	city = models.city_profile_data(
		city_id = city_id,
		city_name = city_name,
		country = country,
		state = state,
		post_code =  postcode,
		population =  population,
		area = area,
		council_name = council_name ,
		contact_email = contact_email,
		contact_number = contact_number,
		council_address = council_address)
	db.session.add(city)
	db.session.commit()

	#insert new user, assign city_admin
	u = models.user_data(
		first_name=contact_firstname, 
		last_name = contact_lastname, 
		password=hash, 
		city_id_admin=city_id, 
		email=email)
	db.session.add(u)
	db.session.commit()
	db.session.close()

	return 'true'

@app.route('/getUserData')
@auth.login_required
def getUserData():
	if 'email' in session:
		email=session['email'].strip()
		userData = models.user_data.query.filter(models.user_data.email == email).all()
		list = [i.returnString() for i in userData]
		return Response(json.dumps(list[0]), mimetype='application/json')
	else:
		return 'false'

	
@app.route('/getCityProfile')
def getCityProfile():
	city_id = request.values.get("city")
	if city_id:
		city_id = city_id.strip()
		profiles = db.session\
			.query(models.showUsers)\
			.filter(models.showUsers.city_id == city_id)\
			.all()
		list = [i.returnString() for i in profiles]
		return Response(json.dumps(list[0]), mimetype='application/json')
	else:
		profiles = db.session.query(models.showUsers).all()
		list = [i.returnString() for i in profiles]
		return Response(json.dumps(list), mimetype='application/json')

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
