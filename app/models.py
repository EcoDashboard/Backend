from sqlalchemy import Table, Column, Integer, \
        String, MetaData, join, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import column_property
from app import db 

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
    ind_id = db.Column(db.Integer, primary_key = True)
    ind_name = db.Column(db.String(100), unique=False)
    designation = db.Column(db.String(100), unique=False)
    unit = db.Column(db.String(100), unique=False)
    description = db.Column(db.String(200), unique=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category_def.cat_id'))
    weight = db.Column(db.Integer, unique=False)
    upper_value = db.Column(db.Integer, unique=False)
    lower_value = db.Column(db.Integer, unique=False)
    target_value = db.Column(db.Integer, unique=False)

    def __repr__(self):
        return '<indicator_def %r>' % (self.ind_id ) 

class category_def(db.Model):
    __tablename__ = 'category_def'
    cat_id = db.Column(db.Integer, primary_key = True)
    cat_name = db.Column(db.String(100), unique=False)
    cat_id_parent = db.Column(db.String(10), unique=False)
    weight = db.Column(db.Integer, unique=False)

    def __repr__(self):
        return '<category_def %r>' % (self.cat_id)

metadata = MetaData()

indicator_def_join = Table('indicator_def', metadata,
	Column('ind_id', Integer, primary_key=True),
        Column('ind_name', String),
        Column( 'designation', String),
	Column('unit', String),
        Column('description', String),
        Column( 'designation', String),	
        Column( 'weight', Integer),
        Column( 'upper_value', Integer),	
        Column('lower_value', Integer),
        Column( 'target_value', Integer),
	Column('category_id', Integer, ForeignKey('category_def.cat_id'))
        )

category_def_join = Table( 'category_def', metadata,
	Column('cat_id', Integer, primary_key=True),
	Column('cat_name', String)	            
	)

showIndcator_join = indicator_def_join.join(category_def_join)
Base = declarative_base()

class showIndicators(Base):
    __table__ = showIndcator_join
    ind_id = indicator_def_join.c.ind_id
    cat_name = category_def_join.c.cat_name
    ind_name = indicator_def_join.c.ind_name
    designation	= indicator_def_join.c.designation
    unit = indicator_def_join.c.unit
    description = indicator_def_join.c.description
    category_id = indicator_def_join.c.category_id
    cat_name = category_def_join.c.cat_name
    weight = indicator_def_join.c.weight
    upper_value = indicator_def_join.c.upper_value
    lower_value = indicator_def_join.c.lower_value
    target_value = indicator_def_join.c.target_value

    def returnString(self):
    	return { 'ind_id' : self.ind_id,
		'cat_name' : self.cat_name,
	        'ind_name' : self.ind_name,
	        'designation' : self.designation,
	        'unit' : self.unit,
	        'description' : self.description,
	        'category_id' : self.category_id,
	        'cat_name' : self.cat_name,
	        'weight' : int(self.weight),
	        'upper_value' : int(self.upper_value),
	        'lower_value' : int(self.lower_value),
	        'target_value' : int(self.target_value)
		}
