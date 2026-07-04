from flask import current_app as app
from dep.models import db,User,Role
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash,generate_password_hash
from flask_security import login_user, current_user
import re

api = Blueprint("api", __name__)


@api.route("/signin", methods=["POST"])
def signin():
    email = request.json.get("email", "")
    password = request.json.get("password", "")

    user = app.security.datastore.find_user(email=email)

    if (user is None or 
        not check_password_hash(user.password, password)):
        return {"message": "Invalid email or password", "code": "ERROR0001"}, 404
    

    login_user(user)

    return {"token": user.get_auth_token(), "roles": user.get_roles()}

@api.route("/trekker/register",methods=["POST"])
def register():
    name=request.json.get('name','')
    email=request.json.get('email','')
    password=request.json.get('password','')

    if not email or not re.match("\w+@\w+[.][a-z]+",email):
        return {"message":"Invalid Email","code":"ERROR0002"},400
    
    if not name:
        return {"message":"Name Required","code":"ERROR0003"},400
    
    if len(password)<6:
        return {"message":"Password length should be atleast 6","code":"ERROR0004"},400
    
    trekker = app.security.datastore.find_user(email=email)

    if trekker:
        return {"message":"User Already Exists!","code":"ERROR0005"},409
    
    user = app.security.datastore.create_user(name=name,email=email,password=generate_password_hash(password))
    role = app.security.datastore.find_role("trekker")
    user.roles.append(role)
    db.session.commit()
    return {"message":"User Created Successfully"},201

@api.route('/admin/getStaffs')
def getStaffs():
    staffs = User.query.join(User.roles).filter(Role.name == "staff").all()
    return jsonify([{"id": user.id,"name": user.name,"email": user.email}for user in staffs])

 