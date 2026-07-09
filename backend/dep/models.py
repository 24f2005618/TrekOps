from flask_sqlalchemy import SQLAlchemy
from flask_security.models import fsqla_v3 as fsqla
from sqlalchemy.orm import backref


# Create database connection object
db = SQLAlchemy()

fsqla.FsModels.set_db_info(db)

class Role(db.Model, fsqla.FsRoleMixin):
    pass


class User(db.Model, fsqla.FsUserMixin):
    name = db.Column(db.String(), nullable=False)

    def get_roles(self):
        return [role.name for role in self.roles]

class Staff(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    phone = db.Column(db.String(10))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    treks = db.relationship('Trek',backref='staff',lazy=True)
    user = db.relationship('User',backref=backref('staff',uselist=False),lazy=True)

class Trekker(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    phone = db.Column(db.String(10))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    bookings = db.relationship('Bookings',backref='trekker',lazy=True)
    user = db.relationship('User',backref=backref('trekker',uselist=False),lazy=True)

class Route(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String())
    location = db.Column(db.String())
    difficulty = db.Column(db.String(1)) #H-hard , M - Medium , E- Easy
    description = db.Column(db.String())
    image_url = db.Column(db.String())
    coordinates = db.Column(db.String()) #optional for map api

class Trek(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    route_id = db.Column(db.Integer,db.ForeignKey('route.id'))
    route = db.relationship('Route',backref=backref('treks',lazy=True),lazy=True)
    available_slots = db.Column(db.Integer)
    total_slots = db.Column(db.Integer)
    staff_id = db.Column(db.Integer,db.ForeignKey('staff.id'))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    reporting_time = db.Column(db.Time)
    status = db.Column(db.String(),default='O') #O- open , C - Closed 


class Bookings(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    trekker_id = db.Column(db.Integer,db.ForeignKey('trekker.id'))
    trek_id = db.Column(db.Integer,db.ForeignKey('trek.id'))
    booking_date = db.Column(db.Date,default=db.func.current_date())
    status = db.Column(db.String(1),default='B') #B-Booked , C- Cancelled , D- Done
    trek = db.relationship('Trek',backref=backref('bookings',lazy=True))
    __table_args__ = (db.UniqueConstraint('trekker_id', 'trek_id', 'status', name='unique_booking'),)

    

