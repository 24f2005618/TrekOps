from flask import current_app as app
from dep.models import db,User,Role, Staff,Trekker,Route,Trek,Bookings
from flask import Blueprint, request, jsonify, json, send_from_directory
from werkzeug.security import check_password_hash,generate_password_hash
from werkzeug.utils import secure_filename
from flask_security import login_user, current_user, roles_required, auth_required, logout_user
import re
from datetime import date,datetime
import os

api = Blueprint("api", __name__)

DIFFICULTY_LABELS = {
    "H": "Hard",    
    "M": "Medium",
    "E": "Easy"
}


def normalize_difficulty(value):
    if value in DIFFICULTY_LABELS:
        return value
    for code, label in DIFFICULTY_LABELS.items():
        if value == label:
            return code
    return value


def serialize_route(route):
    if not route:
        return None
    return {
        "id": route.id,
        "name": route.name,
        "location": route.location,
        "difficulty": DIFFICULTY_LABELS.get(route.difficulty, route.difficulty),
        "difficulty_code": route.difficulty,
        "description": route.description,
        "image_url": route.image_url,
        "coordinates": route.coordinates,
    }


def serialize_trek(trek):
    route = serialize_route(trek.route)
    return {
        "id": trek.id,
        "route_id": trek.route_id,
        "name": route["name"] if route else None,
        "location": route["location"] if route else None,
        "difficulty": route["difficulty"] if route else None,
        "slots": trek.available_slots,
        "total_slots": trek.total_slots,
        "status": trek.status,
        "staff_id": trek.staff_id,
        "reporting_time": trek.reporting_time.strftime("%H:%M") if trek.reporting_time else None,
        "start_date": trek.start_date.strftime("%Y-%m-%d") if trek.start_date else None,
        "end_date": trek.end_date.strftime("%Y-%m-%d") if trek.end_date else None,
        "description": route["description"] if route else None,
        "image_url": route["image_url"] if route else None,
        "coordinates": route["coordinates"] if route else None,
    }


@api.route("/fetchUser", methods=["GET"])
@auth_required('token')
def fetch_user():
    user = current_user
    return {"roles": user.get_roles(),"token": user.get_auth_token(), "active": user.active}, 200

@api.route("/logout", methods=["POST"])
@auth_required('token')
def logout():
    user = current_user
    logout_user(user)
    return {"message": "Logged out successfully"}, 200

@api.route("/signin", methods=["POST"])
def signin():
    email = request.json.get("email", "")
    password = request.json.get("password", "")

    user = app.security.datastore.find_user(email=email)
    if (user is None or 
        not check_password_hash(user.password, password)):
        return {"message": "Invalid email or password", "code": "ERROR0001"}, 404
    if (not user.active):
        return {"message":"User Disabled! Contact Administrator","code":"ERROR0008"},403

    login_user(user)

    return {"token": user.get_auth_token(), "roles": user.get_roles(), "active": user.active}, 200

@api.route("/uploads/<filename>")
def serve_image(filename):
    return send_from_directory("uploads", filename)

@api.route("/trekker/register",methods=["POST"])
def register():
    name=request.json.get('name','')
    email=request.json.get('email','')
    phone=request.json.get('phone','')
    password=request.json.get('password','')


    if not email or not re.match("\w+@\w+[.][a-z]+",email):
        return {"message":"Invalid Email","code":"ERROR0002"},400
    
    if not name:
        return {"message":"Name Required","code":"ERROR0003"},400
    
    if len(phone)!=10 or not phone.isdigit():
        return {"message":"Invalid Phone Number","code":"ERROR0006"},400
    
    if len(password)<6:
        return {"message":"Password length should be atleast 6","code":"ERROR0004"},400
    
    
    trekker = app.security.datastore.find_user(email=email)

    if trekker:
        return {"message":"User Already Exists!","code":"ERROR0005"},409
    
    user = app.security.datastore.create_user(name=name,email=email,password=generate_password_hash(password))
    role = app.security.datastore.find_role("trekker")
    user.roles.append(role)
    db.session.flush()
    trekker = Trekker(user_id=user.id,phone=phone)
    db.session.add(trekker)
    db.session.commit()
    return {"message":"User Created Successfully"},201

@api.route('/staff/register',methods=["POST"])
@auth_required('token')
@roles_required('admin')
def add_staff():
    name=request.json.get('name','')
    email=request.json.get('email','')
    phone=request.json.get('phone','')
    password=request.json.get('password','')

    if not email or not re.match("\w+@\w+[.][a-z]+",email):
        return {"message":"Invalid Email","code":"ERROR0002"},400
    
    if not name:
        return {"message":"Name Required","code":"ERROR0003"},400
    
    if len(password)<6:
        return {"message":"Password length should be atleast 6","code":"ERROR0004"},400
    
    if len(phone)!=10 or not phone.isdigit():
        return {"message":"Invalid Phone Number","code":"ERROR0006"},400
    
    staff = app.security.datastore.find_user(email=email)

    if staff:
        return {"message":"User Already Exists!","code":"ERROR0005"},409
    
    user = app.security.datastore.create_user(name=name,email=email,password=generate_password_hash(password))
    role = app.security.datastore.find_role("staff")
    user.roles.append(role)
    db.session.flush()
    staff = Staff(phone=phone,user_id=user.id)
    db.session.add(staff)
    db.session.commit()
    return {"message":"Staff Created Successfully"},201

@api.route('/getUserName',methods=["GET"])
@auth_required('token')
def get_user_name():
    user = current_user
    if not user:
        return {"message":"User Not Found","code":"ERROR0007"},404
    return {"name": user.name},200


@api.route('/getStats',methods=["GET"])
@auth_required('token')
@roles_required('admin')
def get_stats():
    staff=Staff.query.count()
    trekkers=Trekker.query.count()
    treks=Trek.query.count()
    bookings=Bookings.query.count()
    recent_bookings = Bookings.query.order_by(Bookings.booking_date.desc()).limit(5).all()
    return jsonify({
        "staff": staff,
        "trekkers": trekkers,
        "treks": treks,
        "bookings": bookings,
        "recent_bookings": [{
                "id": booking.id,
                "trekker_name": booking.trekker.user.name,
            "trek_name": booking.trek.route.name, 
                "booking_date": booking.booking_date.strftime("%d-%m-%Y"),
            "location": booking.trek.route.location,
                "status":booking.status}
                for booking in recent_bookings]
    })

@api.route('/getStaffs',methods=["GET"])
@auth_required('token')
@roles_required('admin')
def get_staffs():
    staffs = Staff.query.all()
    return jsonify([{"id": staff.id,"name": staff.user.name,"email": staff.user.email,"phone": staff.phone,"active": staff.user.active}for staff in staffs])

@api.route('/getTrekkers',methods=["GET"])
@auth_required('token')
@roles_required('admin')
def get_trekkers():
    trekkers = Trekker.query.all()
    return jsonify([{"id": trekker.id,"name": trekker.user.name,"email": trekker.user.email,"phone": trekker.phone,"active": trekker.user.active}for trekker in trekkers])

@api.route('/admin/getTreks',methods=["GET"])
@auth_required('token')
@roles_required('admin')
def get_treks_admin():
    treks = Trek.query.all()
    return jsonify([serialize_trek(trek) for trek in treks])


@api.route('/admin/getRoutes',methods=["GET"])
@auth_required('token')
@roles_required('admin')
def get_routes_admin():
    routes = Route.query.all()
    return jsonify([serialize_route(route) for route in routes])


@api.route('/admin/getRoute',methods=["POST"])
@auth_required('token')
@roles_required('admin')
def get_route_admin():
    route_id = request.json.get('id','')
    route = Route.query.get(route_id)
    if not route:
        return {"message":"Route Not Found","code":"ERROR0022"},404
    return jsonify(serialize_route(route))


@api.route('/admin/addRoute',methods=["POST"])
@auth_required('token')
@roles_required('admin')
def add_route():
    form = json.loads(request.form.get("form", "{}"))
    name = form.get("name", "")
    location = form.get("location", "")
    difficulty = normalize_difficulty(form.get("difficulty", ""))
    description = form.get("description", "")
    coordinates = form.get("coordinates", "")
    image = request.files.get("image")

    if not name:
        return {"message":"Name Required","code":"ERROR0003"},400

    if not location:
        return {"message":"Location Required","code":"ERROR0010"},400

    if difficulty not in DIFFICULTY_LABELS:
        return {"message":"Difficulty Required","code":"ERROR0011"},400

    filename = None
    if image and image.filename:
        filename = secure_filename(image.filename)
        image.save(os.path.join("uploads", filename))

    route = Route(
        name=name,
        location=location,
        difficulty=difficulty,
        description=description,
        image_url=filename,
        coordinates=coordinates,
    )
    db.session.add(route)
    db.session.commit()
    return {"message":"Route Created Successfully"},201


@api.route('/admin/deleteRoute',methods=["DELETE"])
@auth_required('token')
@roles_required('admin')
def delete_route():
    route_id = request.json.get('id','')
    route = Route.query.get(route_id)
    if not route:
        return {"message":"Route Not Found","code":"ERROR0022"},404
    if route.treks:
        return {"message":"Cannot delete route with existing treks","code":"ERROR0023"},400
    image_url = route.image_url
    if image_url:
        filename = secure_filename(image_url)
        os.remove(os.path.join("uploads", filename))
    db.session.delete(route)
    db.session.commit()
    return {"message":"Route Deleted Successfully"},204

@api.route('/admin/getTrek',methods=["POST"])
@auth_required('token')
@roles_required('admin')
def get_trek():
    trek_id = request.json.get('id','')
    trek = Trek.query.get(trek_id)
    if not trek:
        return {"message":"Trek Not Found","code":"ERROR0016"},404
    return jsonify(serialize_trek(trek))

@api.route('/admin/deleteTrek',methods=["DELETE"])
@auth_required('token')
@roles_required('admin')
def delete_trek():
    trek_id = request.json.get('id','')
    trek = Trek.query.get(trek_id)
    if not trek:
        return {"message":"Trek Not Found","code":"ERROR0016"},404
    if trek.bookings:
        return {"message":"Cannot delete trek with existing bookings","code":"ERROR0021"},400
    db.session.delete(trek)
    db.session.commit()
    return {"message":"Trek Deleted Successfully"},204

@api.route('/admin/addTrek',methods=["POST"])
@auth_required('token')
@roles_required('admin')
def add_trek():
    form = json.loads(request.form.get("form", "{}"))
    route_id = form.get("route_id", "")
    slots = form.get("slots", "")
    staff_id = form.get("staff_id", "")
    reporting_time = form.get("reporting_time", "")
    trek_date = form.get("start_date", "")
    end_date = form.get("end_date", "")

    start_date = datetime.strptime(trek_date,"%Y-%m-%d").date() if trek_date else None
    end_date = datetime.strptime(end_date,"%Y-%m-%d").date() if end_date else None

    if not route_id:
        return {"message":"Route Required","code":"ERROR0010"},400

    if not slots:
        return {"message":"Slots Required","code":"ERROR0011"},400

    if not staff_id:
        return {"message":"Staff ID Required","code":"ERROR0012"},400

    if not reporting_time:
        return {"message":"Reporting Time Invalid","code":"ERROR0013"},400

    try:
        reporting_time = datetime.strptime(reporting_time, "%H:%M").time()
    except ValueError:
        return {"message":"Reporting Time Invalid","code":"ERROR0013"},400

    try:
        route_id = int(route_id)
        slots = int(slots)
        staff_id = int(staff_id)
    except (TypeError, ValueError):
        return {"message":"Invalid Trek Data","code":"ERROR0011"},400

    route = Route.query.get(route_id)
    if not route:
        return {"message":"Route Not Found","code":"ERROR0022"},404

    if not start_date or start_date < date.today():
        return {"message":"Trek Date Invalid","code":"ERROR0014"},400

    if not end_date or end_date<start_date:
        return {"message":"End Date Invalid","code":"ERROR0015"},400
    staff = Staff.query.get(staff_id)
    if not staff:
        return {"message":"Staff Not Found","code":"ERROR0007"},404
    for trek in staff.treks:
        if trek.status!='D' and (trek.start_date <= start_date <= trek.end_date or \
            trek.start_date <= end_date <= trek.end_date):
            return jsonify({"message": "Staff is already assigned to another trek with same time range"}), 400

    trek = Trek(route_id=route_id,
            total_slots=slots,available_slots=slots,
            staff_id=staff_id,reporting_time=reporting_time,
            start_date=start_date,end_date=end_date)
    db.session.add(trek)
    db.session.commit()
    return {"message":"Trek Created Successfully"},201

@api.route('/admin/editTrek',methods=["PATCH"])
@auth_required('token')
@roles_required('admin')
def edit_trek():
    form = json.loads(request.form.get("form", "{}"))
    trek_id = form.get("id", "")
    route_id = form.get("route_id", "")
    slots = form.get("slots", "")
    staff_id = form.get("staff_id", "")
    reporting_time = form.get("reporting_time", "")
    start_date_str = form.get("start_date", "")
    end_date_str = form.get("end_date", "")

    start_date = datetime.strptime(start_date_str,"%Y-%m-%d").date() if start_date_str else None
    end_date = datetime.strptime(end_date_str,"%Y-%m-%d").date() if end_date_str else None

    trek = Trek.query.get(trek_id)
    if not trek:
        return {"message":"Trek Not Found","code":"ERROR0016"},404

    try:
        route_id = int(route_id) if route_id else None
        slots = int(slots) if slots else None
        staff_id = int(staff_id) if staff_id else None
    except (TypeError, ValueError):
        return {"message":"Invalid Trek Data","code":"ERROR0011"},400

    if route_id:
        route = Route.query.get(route_id)
        if not route:
            return {"message":"Route Not Found","code":"ERROR0022"},404

    if staff_id:
        staff = Staff.query.get(staff_id)
        if not staff:
            return {"message":"Staff Not Found","code":"ERROR0007"},404
    else:
        staff = trek.staff

    if start_date and start_date < date.today():
        return {"message":"Trek Date Invalid","code":"ERROR0014"},400

    if end_date and end_date < start_date:
        return {"message":"End Date Invalid","code":"ERROR0015"},400

    for etrek in staff.treks:
        if etrek.id == trek.id or etrek.status == 'D':
            continue
        if start_date <= etrek.end_date and \
            etrek.start_date <= end_date:
            return jsonify({"message": "Staff is already assigned to another trek with same time range"}), 400

    if slots:
        trek.total_slots=slots
        trek.available_slots=slots
    if staff_id:
        trek.staff_id=staff_id
    if reporting_time:
        try:
            reporting_time_obj = datetime.strptime(reporting_time, "%H:%M").time()
            trek.reporting_time=reporting_time_obj
        except ValueError:
            return {"message":"Reporting Time Invalid","code":"ERROR0013"},400
    if start_date:
        trek.start_date=start_date
    if end_date:
        trek.end_date=end_date
    if route_id:
        trek.route_id=route_id

    db.session.commit()
    return {"message":"Trek Updated Successfully"},204

@api.route('/admin/getBookings',methods=["GET"])
@auth_required('token')
@roles_required('admin')
def get_bookings_admin():
    bookings = Bookings.query.all()
    return jsonify([{
        "id":booking.id,
        "trekker_name":booking.trekker.user.name,
        "trek_name":booking.trek.route.name,
        "location":booking.trek.route.location,
        "booking_date":booking.booking_date.strftime("%d-%m-%Y"),
        "status": booking.status
    }for booking in bookings])

@api.route('/toggleStaffStatus',methods=["PATCH"])
@auth_required('token')
@roles_required('admin')
def toggle_staff_status():
    staff_id = request.json.get('id','')
    staff = Staff.query.get(staff_id)
    if not staff:
        return {"message":"Staff Not Found","code":"ERROR0007"},404
    staff.user.active = not staff.user.active
    db.session.commit()
    return {"message":"Staff Status Updated Successfully"},204

@api.route('/toggleTrekkerStatus',methods=["PATCH"])
@auth_required('token')
@roles_required('admin')
def toggle_trekker_status():
    trekker_id = request.json.get('id','')
    trekker = Trekker.query.get(trekker_id)
    if not trekker:
        return {"message":"Trekker Not Found","code":"ERROR0009"},404
    trekker.user.active = not trekker.user.active
    db.session.commit()
    return {"message":"Trekker Status Updated Successfully"},204

@api.route('/trekker/getStats',methods=["GET"])
@auth_required('token')
@roles_required('trekker')
def get_stats_trekker():
    trekker = current_user.trekker
    upcoming_treks_count = Bookings.query.filter_by(trekker_id=trekker.id, status='B').filter(
                            db.or_(db.and_(Bookings.trek.has(Trek.start_date == date.today()),
                            Bookings.trek.has(Trek.reporting_time >= datetime.now().time())), 
                            Bookings.trek.has(Trek.start_date > date.today()))).count()
    completed_treks_count = Bookings.query.filter_by(trekker_id=trekker.id, status='D').count()
    available_treks = Trek.query.filter(
                            db.and_(Trek.status == 'O',
                            db.or_(db.and_(Trek.start_date == date.today(), Trek.reporting_time >= datetime.now().time()), 
                            Trek.start_date > date.today())))
    recent_bookings = Bookings.query.filter_by(trekker_id=trekker.id, status='B').order_by(Bookings.booking_date.desc()).limit(3).all()
    return jsonify({
        "count":{
            "upcoming_treks": upcoming_treks_count,
            "completed_treks": completed_treks_count,
            "available_treks": available_treks.count(),
        },
        "available_treks": [{
            "id": trek.id,
            "name": trek.route.name,
            "location": trek.route.location,
            "difficulty": trek.route.difficulty,
            "duration": (trek.end_date - trek.start_date).days,
            "slots": trek.available_slots,
            "image_url": trek.route.image_url
        } for trek in available_treks.limit(4).all()],
        "recent_bookings": [{
            "trek_name": booking.trek.route.name,
            "location": booking.trek.route.location,
            "status": booking.status
        } for booking in recent_bookings]
    })




@api.route('/trekker/getTreks', methods=["GET"])
@auth_required('token')
@roles_required('trekker')
def get_treks_trekker():
    treks = (
        Trek.query.filter(db.and_(Trek.status == 'O',db.or_(db.and_(Trek.start_date == date.today(), Trek.reporting_time >= datetime.now().time()), Trek.start_date > date.today()))).all()
    )

    return jsonify([
        {
            "id": trek.id,
            "name": trek.route.name,
            "location": trek.route.location,
            "difficulty": DIFFICULTY_LABELS.get(trek.route.difficulty, trek.route.difficulty),
            "slots": trek.available_slots,
            "duration": (trek.end_date - trek.start_date).days,
            "image_url": trek.route.image_url
        }
        for trek in treks
    ])

@api.route('/trekker/getTrek',methods=["POST"])
@auth_required('token')
@roles_required('trekker')
def get_trek_trekker():
    trek_id = request.json.get('id','')
    trek = Trek.query.get(trek_id)
    if not trek:
        return {"message":"Trek Not Found","code":"ERROR0016"},404
    return jsonify(serialize_trek(trek))
@api.route('/trekker/bookTrek',methods=["POST"])
@auth_required('token')
@roles_required('trekker')
def book_trek():
    trek_id = request.json.get('id','')
    trek = Trek.query.get(trek_id)
    if not trek:
        return {"message":"Trek Not Found","code":"ERROR0016"},404
    if trek.available_slots<=0:
        return {"message":"No Slots Available","code":"ERROR0017"},400
    if Bookings.query.filter_by(trekker_id=current_user.trekker.id,trek_id=trek.id,status='B').first():
        return {"message":"Trek Already Booked","code":"ERROR0018"},400
    booking = Bookings(trekker_id=current_user.trekker.id,trek_id=trek.id)
    trek.available_slots-=1
    trek.status = 'C' if trek.available_slots==0 else 'O'
    db.session.add(booking)
    db.session.commit()
    return {"message":"Trek Booked Successfully"},201

@api.route('/trekker/getBookings',methods=["GET"])
@auth_required('token')
@roles_required('trekker')
def get_bookings_trekker():
    bookings = Bookings.query.filter_by(trekker_id=current_user.trekker.id,status='B').all()
    if not bookings:
        return jsonify([]),200
    return jsonify([{
        "id":booking.id,
        "trek_name":booking.trek.route.name,
        "location":booking.trek.route.location,
        "staff":booking.trek.staff.user.name,
        "reporting_time":booking.trek.reporting_time.strftime("%H:%M %p") if booking.trek.reporting_time else None,
        "start_date":booking.trek.start_date.strftime("%d-%m-%Y") if booking.trek.start_date else None,
        "end_date":booking.trek.end_date.strftime("%d-%m-%Y") if booking.trek.end_date else None
    }for booking in bookings])

@api.route('/trekker/cancelBooking',methods=["PATCH"])
@auth_required('token')
@roles_required('trekker')
def cancel_booking():
    booking_id = request.json.get('id','')
    booking = Bookings.query.get(booking_id)
    if not booking:
        return {"message": "Booking Not Found","code":"ERROR0019"},404
    if booking.trekker_id != current_user.trekker.id:
        return {"message": "Unauthorized","code":"ERROR0020"},403
    booking.status = 'C' # Cancelled
    booking.trek.available_slots += 1
    db.session.commit()
    return {"message": "Booking Cancelled Successfully"},204

@api.route('/trekker/getHistory',methods=["GET"])
@auth_required('token')
@roles_required('trekker')
def get_history_trekker():
    bookings = Bookings.query.filter_by(trekker_id=current_user.trekker.id).filter(Bookings.status.in_(['C', 'D'])).all()
    return jsonify([{
        "id":booking.id,
        "trek_name":booking.trek.route.name,
        "location":booking.trek.route.location,
        "staff":booking.trek.staff.user.name,
        "reporting_time":booking.trek.reporting_time.strftime("%H:%M %p") if booking.trek.reporting_time else None,
        "start_date":booking.trek.start_date.strftime("%d-%m-%Y") if booking.trek.start_date else None,
        "end_date":booking.trek.end_date.strftime("%d-%m-%Y") if booking.trek.end_date else None,
        "status": booking.status
    }for booking in bookings])

@api.route('/getProfile',methods=["GET"])
@auth_required('token')
# @roles_required('trekker','staff')
def get_profile():
    user = current_user
    if user.has_role('trekker'):
        trekker = user.trekker
        return jsonify({
            "name": user.name,
            "email": user.email,
            "phone": trekker.phone
        })
    elif user.has_role('staff'):
        staff = user.staff
        return jsonify({
            "name": user.name,
            "email": user.email,
            "phone": staff.phone,
        })
    else:
        return {"message":"User Role Not Found","code":"ERROR0024"},404

@api.route('/updateProfile',methods=["PATCH"])
@auth_required('token')
def update_profile():
    user = current_user
    name = request.json.get('name','')
    email = request.json.get('email','')
    phone = request.json.get('phone','')
    password = request.json.get('password','')
    if(not check_password_hash(user.password,password)):
        return {"message":"Incorrect Password","code":"ERROR0025"},403
    if not email or not re.match("\w+@\w+[.][a-z]+",email):
        return {"message":"Invalid Email","code":"ERROR0002"},400
    
    if not name:
        return {"message":"Name Required","code":"ERROR0003"},400
    
    if len(phone)!=10 or not phone.isdigit():
        return {"message":"Invalid Phone Number","code":"ERROR0006"},400
    user.name = name
    user.email = email
    if user.has_role('trekker'):
        user.trekker.phone = phone
    elif user.has_role('staff'):
        user.staff.phone = phone
    db.session.commit()
    return {"message":"Profile Updated Successfully"},204

@api.route('/editPassword',methods=["PATCH"])
@auth_required('token')
def edit_password():
    user = current_user
    old_password = request.json.get('current_password','')
    new_password = request.json.get('new_password','')
    confirm_password = request.json.get('confirm_password','')
    if new_password != confirm_password:
        return {"message":"New Password and Confirm Password do not match","code":"ERROR0026"},400
    if(not check_password_hash(user.password,old_password)):
        return {"message":"Incorrect Current Password","code":"ERROR0025"},403
    if len(new_password)<6:
        return {"message":"Password length should be atleast 6","code":"ERROR0004"},400
    user.password = generate_password_hash(new_password)
    db.session.commit()
    return {"message":"Password Updated Successfully"},204

@api.route('/staff/getTreks',methods=["GET"])
@auth_required('token')
@roles_required('staff')
def get_treks_staff():
    current_staff = current_user.staff
    treks = [trek for trek in current_staff.treks]
    return jsonify([{
        "id": trek.id,
        "trek_name": trek.route.name,
        "location": trek.route.location,
        "slots": trek.available_slots,
        "duration": (trek.end_date - trek.start_date).days,
        "status": trek.status,
        "participants": len([booking for booking in trek.bookings if booking.status == 'B'])
    } for trek in treks])

@api.route('/staff/getTrek',methods=["POST"])
@auth_required('token')
@roles_required('staff')
def get_trek_staff():
    trek_id = request.json.get('id','')
    trek = Trek.query.get(trek_id)
    participants = [{'name': booking.trekker.user.name,
                    'email': booking.trekker.user.email,
                    'phone' : booking.trekker.phone,
                    'booking_date': booking.booking_date.strftime("%d-%m-%Y")
                    } for booking in trek.bookings if booking.status in ['B', 'D']] if trek else []
    if not trek:
        return {"message":"Trek Not Found","code":"ERROR0016"},404
    if trek.staff_id != current_user.staff.id:
        return {"message": "Unauthorized","code":"ERROR0020"},403
    return jsonify({
        'trek_name' : trek.route.name,
        'location' : trek.route.location,
        'start_date' : trek.start_date.strftime("%d-%m-%Y") if trek.start_date else None,
        'end_date' : trek.end_date.strftime("%d-%m-%Y") if trek.end_date else None,
        'available_slots' : trek.available_slots,
        'total_slots' : trek.total_slots,
        'status' : trek.status,
        'participants' : participants,
        'image_url' : trek.route.image_url
    })

@api.route('/staff/toggleTrekStatus',methods=["PATCH"])
@auth_required('token')
@roles_required('staff')
def toggle_trek_status():
    trek_id = request.json.get('id','')
    trek = Trek.query.get(trek_id)
    if not trek:
        return {"message":"Trek Not Found","code":"ERROR0016"},404
    if trek.staff_id != current_user.staff.id:
        return {"message": "Unauthorized","code":"ERROR0020"},403
    trek.status = 'C' if trek.status == 'O' else 'O'
    db.session.commit()
    return {"message":"Trek Status Updated Successfully"},204

@api.route('/staff/completeTrek',methods=["PATCH"])
@auth_required('token')
@roles_required('staff')
def complete_trek():
    trek_id = request.json.get('id','')
    trek = Trek.query.get(trek_id)
    if not trek:
        return {"message":"Trek Not Found","code":"ERROR0016"},404
    if trek.staff_id != current_user.staff.id:
        return {"message": "Unauthorized","code":"ERROR0020"},403
    trek.status = 'D'
    for booking in trek.bookings:
        if booking.status == 'B':
            booking.status = 'D'
    db.session.commit()
    return {"message":"Trek Completed Successfully"},204

@api.route('/staff/getParticipants',methods=["GET"])
@auth_required('token')
@roles_required('staff')
def get_participants():
    current_staff = current_user.staff
    participants = [{
        "name": booking.trekker.user.name,
        "email": booking.trekker.user.email,
        "phone": booking.trekker.phone,
        "booking_date": booking.booking_date.strftime("%d-%m-%Y"),
        "booking_status": booking.status
    } for trek in current_staff.treks for booking in trek.bookings if booking.status in ['B', 'D']]
    return jsonify(participants)

@api.route('/staff/getStats',methods=["GET"])
@auth_required('token')
@roles_required('staff')
def get_stats_staff():
    current_staff = current_user.staff
    completed_treks_len = len([trek for trek in current_staff.treks if trek.status == 'D'])
    upcoming_treks = [trek for trek in current_staff.treks if trek.status != 'D' and (trek.start_date > date.today() or (trek.start_date == date.today() and trek.reporting_time >= datetime.now().time()))]
    current_trek = Trek.query.filter_by(staff_id=current_staff.id).filter(
                    db.and_(Trek.status!='D', db.or_(
                        date.today() > Trek.start_date, 
                        db.and_(date.today() == Trek.start_date, 
                        datetime.now().time() >= Trek.reporting_time)),
                        date.today()<=Trek.end_date)).first()
    next_trek = Trek.query.filter_by(staff_id=current_staff.id).filter(
        db.and_(Trek.status!='D', db.or_(
            Trek.start_date > date.today(),db.and_(
            Trek.start_date == date.today(), Trek.reporting_time >= datetime.now().time())))
            ).order_by(Trek.start_date.asc()).offset(1).first()
    return jsonify({
        "count": {
        "completed_treks": completed_treks_len,
        "upcoming_treks": len(upcoming_treks)
        },
        "upcoming_treks": [{
            "id": trek.id,
            "trek_name": trek.route.name,
            "location": trek.route.location,
            "slots": trek.available_slots,
            "duration": (trek.end_date - trek.start_date).days,
            "status": trek.status,
            "image_url": trek.route.image_url
        } for trek in upcoming_treks],
        "current_trek": {
            "id": current_trek.id,
            "trek_name": current_trek.route.name,
            "location": current_trek.route.location,
            "participants": current_trek.total_slots-current_trek.available_slots,
            "image_url": current_trek.route.image_url
        } if current_trek else None
    })
