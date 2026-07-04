from flask_sqlalchemy import SQLAlchemy
from flask_security.models import fsqla_v3 as fsqla


# Create database connection object
db = SQLAlchemy()

fsqla.FsModels.set_db_info(db)

class Role(db.Model, fsqla.FsRoleMixin):
    pass


class User(db.Model, fsqla.FsUserMixin):
    name = db.Column(db.String(), nullable=False)
    phone = db.Column(db.Integer,nullable=False)
    status = db.Column(db.String())

    def get_roles(self):
        return [role.name for role in self.roles]

class Trek(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String())
    location = db.Column(db.String())
    difficulty = db.Column(db.String(1)) #H-hard , M - Medium , E- Easy
    duration = db.Column(db.Integer)
    available_slots = db.Column(db.Integer)
    total_slots = db.Column(db.Integer)
    assigned_staff_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(db.String())
    description = db.Column(db.String())
    created_at = db.Column(db.DateTime)

class Bookings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    trek_id = db.Column(db.Integer,db.ForeignKey('trek.id'))
    booking_date = db.Column(db.Date)
    status = db.Column(db.String())
    completed_at = db.Column(db.DateTime)

    

