from sqlalchemy import Table, Column, Integer, \
        String, MetaData, join, ForeignKey,func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import column_property
from app import db 

class city_score_data(db.Model):
	__tablename__ = 'city_score_data'
	score_id = db.Column(db.Integer, primary_key = True)
	city_id = db.Column(db.String(100), unique=False)
	cat_id = db.Column(db.Integer, unique=False)
	score = db.Column(db.Integer, unique=False)
	data_year = db.Column(db.Integer, unique=False)

	def returnString(self):
		return { 'score_id' : self.score_id,
			'city_id' : self.city_id,
			'cat_id': self.cat_id,
			'score' : int(self.score),
			'data_year' : self.data_year,
            'data_year' : self.data_year
		}
	
	def __repr__(self):
		return '<city_score_data %r>' % (self.score_id)
