from flask import Flask
import os
from flask_security import Security, SQLAlchemyUserDatastore
from werkzeug.security import generate_password_hash
from flask_cors import CORS

from dep.models import db, User, Role
from config import Config
from dep.views import api


def create_app():
    # Create app
    app = Flask(__name__)
    
    CORS(app) 

    app.config.from_object(Config)

    db.init_app(app)

    datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, datastore)


    with app.app_context():
        db.create_all()
        if not app.security.datastore.find_role("admin"):
            admin = app.security.datastore.create_role(name="admin")
            staff = app.security.datastore.create_role(name="staff")
            user = app.security.datastore.create_role(name="trekker")
            db.session.flush()

            karan = app.security.datastore.create_user(name="Karan",
                                                         email="karan@mail.com",
                                                         password=generate_password_hash("karan123"))
            karan.roles.append(admin)
            db.session.commit()

    app.register_blueprint(api)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()