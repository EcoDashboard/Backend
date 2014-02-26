from app import app
from app import models, db
from flask import render_template
from flask import request, jsonify, session, escape, Response, g
from flask.ext.cors import cross_origin
from flask.ext.httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import hashlib
import json

auth = HTTPBasicAuth()




users={'naveen':'password','hanwei':123456}

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

@app.route('/login', methods=['GET'])
def loginGet():
	print 'HELLO'
    if 'email' in session:
        return '{email:%s, login=true}' % escape(session['email'])
    return 'false'

@app.route('/login', methods=['POST'])
def loginPost():
	print 'HELLO2'
	email=request.form['email']
	password=request.form['password']

	userInDB = models.user_data.query.filter(models.user_data.email == email).filter(models.user_data.password == hashlib.sha256(password).hexdigest()).all()

	if len(userInDB) == 1:
		g.user = userInDB[0]
		token = generate_auth_token()
		return token
	else:
		return False


@app.route('/logout', methods=['GET'])
def logout():
	if 'email' in session:
		session.pop('email', None)
		return 'true'

@app.route('/register_test.html')
def registerTest():
	return render_template("register_test.html")

@app.route('/register', methods=['POST'])
@cross_origin()
def register():
	email=request.form['email'].strip()
	if not email:
		return 'email is empty'

	user_name=request.form['user_name']
	password=request.form['password']
	hash = hashlib.sha256(password).hexdigest()
	city_id_admin = request.form['city_id_admin']
	email=request.form['email']

	u = models.user_data(user_name=user_name, password=hash, city_id_admin=city_id_admin, email=email)
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


@app.route('/getCityList', methods=['GET'])
def getCityList():
	cityList = models.city_profile_data.query.all()
	list = [i.returnString() for i in cityList]
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
