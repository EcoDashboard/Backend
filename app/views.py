#lint:disable
from app import app
from app import models, calculator, db, CityDashboard
from flask import render_template
from flask import request, jsonify, session, escape, Response, g, make_response, redirect, url_for
from flask.ext.assets import Environment, Bundle
from flask.ext.cors import cross_origin
from flask.ext.httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy import func
from urlparse import urlparse, urlunparse
from datetime import timedelta
from functools import update_wrapper

import hashlib
import json
import re
import urllib


#Handling SCSS/SASS files
assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('styles/eco.scss', 'styles/main.scss', 'styles/dashboard.scss', filters='pyscss', output='all.css')
assets.register('scss_all', scss)


auth = HTTPBasicAuth()

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

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


# THESE ARE THE ROUTES FOR HTML PAGES

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():

    if 'user' in session:
        return redirect(url_for('home'))

    return render_template('login.html')


# THESE ARE THE ROUTES FOR THE API

@app.route('/login_test.html', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/login', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*', headers=['Content-Type'])
def loginPost():


    email=urllib.unquote(request.form['email'])
    password=request.form['password']

    user = models.user_data.query.filter(models.user_data.email == email)\
        .filter(models.user_data.password == hashlib.sha256(password).hexdigest())\
        .first()

    if user:
        g.user = user
        session['user'] = user
        token = generate_auth_token()
        return redirect(url_for('home'))
    else:
        return make_response("Cannot find user",401)

@app.route('/dashboard', methods=['GET'])
def dashboard():

    return render_template('dashboard.html')

@app.route('/eval.html', methods=['GET'])
def evals():
    return render_template('eval.html')

@app.route('/logout', methods=['GET'])
@crossdomain(origin='*', headers='Content-Type')
def logout():
    if 'user' in session:
        session.pop('user', None)
        return redirect(url_for('home'))
    return redirect(url_for('home'))

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


@app.route('/register', methods=['GET','POST'])
@crossdomain(origin='*', headers='Content-Type')
def register():

    if request.method == 'GET':

      return render_template('register.html')

    elif request.method == 'POST':

      # print request.form

      needed_keys = ['email','password','contact_firstname','contact_lastname', 'city_name']
            #   'city_abbre','city_name','council_name', 'state', 'country',\
            #   'postcode', 'area', 'population', 'contact_email',\
            #   'contact_number', 'council_address']

      print set(needed_keys) - set(request.form.keys())
      print "avail_keys =>", request.form

      key_result = set(needed_keys) - set(request.form.keys())

      if len(key_result) != 0:
          return make_response("Missing form fields\nNeeded keys => %s" % (key_result),503)

      # user
      email = urllib.unquote(request.form['email'].strip()).lower()
      password=request.form['password']
      hash = hashlib.sha256(password).hexdigest()
      contact_firstname = request.form['contact_firstname'].strip()
      contact_lastname = request.form['contact_lastname'].strip()

      print 'User fine'

      # city
    #   city_id = request.form['city_abbre'].strip().upper()
      city_name = request.form['city_name'].strip()
      # council_name = request.form['council_name'].strip()
      # state = request.form['state'].strip()
      # country = request.form['country'].strip()
      # postcode = request.form['postcode'].strip()
      # area = request.form['area'].strip()
      # population = request.form['population'].strip()
      # contact_email = request.form['contact_email'].strip()
      # contact_number = request.form['contact_number'].strip()
      # council_address = request.form['council_address'].strip()
      #
      # check
      errors=[]
      if not email:
          errors.append('Email is empty.')
      elif  models.user_data.query.filter(models.user_data.email == email).first():
          errors.append('Email has already been used.')
      #
      # if not city_id:
      #     errors.append('City abbreviation is empty.')
      # elif checkCityIdExists(city_id):
      #     errors.append('City Alias has already been used.')
      #
      # if not re.match("^[0-9]*[.]?[0-9]+$", area):
      #     errors.append('Area format is incorrect.')
      #
      # # invalid input
      # if errors:
      #     return Response(json.dumps(errors), mimetype='application/json')
      #
      # print "No errors!"

      #insert new city
      # city = models.city_profile_data(
      #     city_id = city_id,
      #     city_name = city_name,
      #     country = country,
      #     state = state,
      #     post_code =  postcode,
      #     population =  population,
      #     area = area,
      #     council_name = council_name ,
      #     contact_email = contact_email,
      #     contact_number = contact_number,
      #     council_address = council_address)
      # db.session.add(city)
      # db.session.commit()

      #insert new user, assign city_admin
      u = models.user_data(
          first_name = contact_firstname,
          last_name = contact_lastname,
          password = hash,
          city_id_admin = city_name,
          email = email)
      db.session.add(u)
      db.session.commit()
      db.session.close()


      return redirect(url_for('home'))

@app.route('/getUserData')
@crossdomain(origin='*')
# @auth.login_required
def getUserData():
    if 'email' in session:
        email=session['email'].strip()
        userData = models.user_data.query.filter(models.user_data.email == email).all()
        list = [i.returnString() for i in userData]
        return Response(json.dumps(list[0]), mimetype='application/json')
    else:
        return 'false'


@app.route('/getCityProfile')
@crossdomain(origin='*', headers='Content-Type')
def getCityProfile():
    city_id = request.values.get("city")
    if city_id:
        city_id = city_id.strip()
        #profiles = db.session\
        #    .query(models.showUsers)\
        #    .filter(models.showUsers.city_id == city_id)\
        #    .all()
        #list = [i.returnString() for i in profiles]
        citydata = getCityProfileByCityId(city_id)
        return Response(json.dumps(citydata), mimetype='application/json')
    else:
        profiles = db.session.query(models.showUsers).all()
        list = [i.returnString() for i in profiles]
        return Response(json.dumps(list), mimetype='application/json')

def getCityProfileByCityId(cityid):
    profiles = db.session\
        .query(models.showUsers)\
        .filter(models.showUsers.city_id == cityid)\
        .all()
    list = [i.returnString() for i in profiles]
    return list[0]

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

@app.route('/calculation_test.html')
def registerTest():
    return render_template("calculation_test.html")

@app.route('/saveScore', methods=['POST','GET'])
@crossdomain(origin='*', headers='Content-Type')
def saveScore():
	post = json.dumps(request.json)
	print post
	score = 0
	decoded = json.loads(post)
	catID = decoded["cat_ID"]
	cat_weight = models.category_def.query.filter_by(cat_id = catID).first().weight / 100
	values = decoded["indicators"]
	query = models.indicator_def.query
	for element in values:
		ind_ID = int(element["ind"][4:])+1
		ind_value = int(element["value"])
		ind_weight = query.get(ind_ID).weight/100
		upper_value = query.get(ind_ID).upper_value
		lower_value = query.get(ind_ID).lower_value
		target_value = query.get(ind_ID).target_value
		if ind_value <= target_value:
			ind_score = (ind_value - lower_value)/(target_value - lower_value)
		elif ind_value >= target_value:
			ind_score = (upper_value - ind_value)/(upper_value - target_value)
		print ind_score
		score += ind_score * ind_weight * cat_weight * 100
	return str(score)
#lint:enable


@app.route('/GetDashboard', methods=['POST','GET'])
@crossdomain(origin='*', headers='Content-Type')
def GetDashboard():

    city_id = request.values.get("city")
    #Get data from database
    cityData = getCityProfileByCityId(city_id)

    city = CityDashboard.CityDashboard()
    city.cityID = cityData["city_id"]
    city.cityName = cityData["city_name"]
    city.cityArea = cityData["area"]
    city.cityPopulation = cityData["population"]
    city.lastProfileUpdateDate = ""

    #set council data
    council = CityDashboard.CityCouncil()
    council.name = cityData["council_name"]
    council.address = cityData["council_address"]
    city.cityCouncilData = council

    #set council contact data
    contact = CityDashboard.ContactInfo()
    contact.name = cityData["first_name"] + " " + cityData["last_name"]
    contact.number = cityData["contact_number"]
    contact.email = cityData["contact_email"]
    city.cityCouncilData.contact = contact

    #finalIndex = CityDashboard.FinalIndex()

    #categories


    return Response(json.dumps(city.returnJson()), mimetype='application/json')
