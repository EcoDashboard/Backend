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
