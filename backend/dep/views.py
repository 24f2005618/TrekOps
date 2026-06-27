from flask import current_app as app
from flask import Blueprint, request
from werkzeug.security import check_password_hash
from flask_security import login_user, current_user

api = Blueprint("api", __name__)


@api.route("/admin", methods=["POST"])
def admin_login():
    email = request.json.get("email", "")
    password = request.json.get("password", "")

    admin = app.security.datastore.find_user(email=email)

    if (admin is None or 
        not check_password_hash(admin.password, password) or 
        not admin.has_role("admin")):
        return {"message": "Invalid email or password", "code": "ERROR0001"}, 404
    
    login_user(admin)

    return {"token": admin.get_auth_token(), "roles": admin.get_roles()}

 