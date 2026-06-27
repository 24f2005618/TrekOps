from flask_sqlalchemy import SQLAlchemy
from flask_security.models import fsqla_v3 as fsqla


# Create database connection object
db = SQLAlchemy()

fsqla.FsModels.set_db_info(db)

class Role(db.Model, fsqla.FsRoleMixin):
    pass


class User(db.Model, fsqla.FsUserMixin):
    name = db.Column(db.String(), nullable=False)

    def get_roles(self):
        return [role.name for role in self.roles]

