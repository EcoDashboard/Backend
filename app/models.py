from app import db
from sqlalchemy import Column, Integer, String

class user_data(db.Model):
    __tablename__ = 'user_data'
    user_id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String(30), unique=False)
    city_id_admin = db.Column(db.String(20), unique=False)
    email = db.Column(db.String(100), unique=False)
    password = db.Column(db.String(50), unique=False)

    def __repr__(self):
        return '<user_data %r>' % (self.user_name)

class indicator_def(db.Model):
    __tablename__ = 'indicator_def'
    ind_id = db.Column(db.String(40), primary_key = True)
    ind_name = db.Column(db.String(100), unique=False)
    designation = db.Column(db.String(100), unique=False)
    unit = db.Column(db.String(100), unique=False)
    description = db.Column(db.String(200), unique=False)
    category_id = db.Column(db.String(40), db.ForeignKey('category_def.cat_id'))
    weight = db.Column(db.Integer, unique=False)
    upper_value = db.Column(db.Integer, unique=False)
    lower_value = db.Column(db.Integer, unique=False)
    target_value = db.Column(db.Integer, unique=False)

    def __repr__(self):
        return '<indicator_def %r>' % (self.ind_id )

class category_def(db.Model):
    __tablename__ = 'category_def'
    cat_id = db.Column(db.String(40), primary_key = True)
    cat_name = db.Column(db.String(100), unique=False)
    cat_id_parent = db.Column(db.String(10), unique=False)
    weight = db.Column(db.Integer, unique=False)

    def __repr__(self):
        return '<category_def %r>' % (self.cat_id)

