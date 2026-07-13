from flask import Flask
import os
from flask_security import Security, SQLAlchemyUserDatastore
from werkzeug.security import generate_password_hash
from flask_cors import CORS
from flask import send_from_directory
from celery import Celery, Task

from dep.models import db, User, Role
from config import Config
from dep.views import api
from extensions import mail,cache

def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


def create_app():
    # Create app
    app = Flask(__name__)
    CORS(app) 

    app.config.from_object(Config)
    

    db.init_app(app)
    mail.init_app(app)
    cache.init_app(app)
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, datastore)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    with app.app_context():
        db.create_all()
        if not app.security.datastore.find_role("admin"):
            admin = app.security.datastore.create_role(name="admin")
            staff = app.security.datastore.create_role(name="staff")
            user = app.security.datastore.create_role(name="trekker")
            db.session.flush()

            karan = app.security.datastore.create_user(name="Karan",
                                                         email="karanasvak@gmail.com",
                                                         password=generate_password_hash("123456"))
            karan.roles.append(admin)
            db.session.commit()

    app.register_blueprint(api)
    celery = celery_init_app(app)
    return app, celery

app,celery = create_app()

import dep.tasks

if __name__ == "__main__":
    app.run()