from celery import shared_task
from flask_mail import Message
from extensions import mail
from datetime import date, timedelta
from dep.models import db, Trek, Bookings, Staff, Trekker, User
from flask import render_template,Response
import csv,io
import os

@shared_task
def send_email(to, subject, body=None, html=None):
    msg = Message(subject, recipients=[to])
    if body: 
        msg.body = body
    if html:
        msg.html = html
    mail.send(msg)
    
@shared_task
def send_daily_remainders():
    tomorrow = date.today() + timedelta(days=1)
    treks = Trek.query.filter_by(start_date=tomorrow).all()
    for trek in treks:
        for booking in trek.bookings:
            email = booking.trekker.user.email
            body= f"""Dear {booking.trekker.user.name},\n
    This is a reminder that you have a trek scheduled for {tomorrow}.\n
Trek Details:\n
    Trek Name: {trek.route.name}\n
    Location: {trek.route.location}\n
    Reporting Time: {trek.reporting_time}\n
Best regards,\nTrekOps Team"""
            send_email.delay(email, "Daily Reminder", body)

        staff = trek.staff
        email = staff.user.email
        body= f"""Dear {staff.user.name},\n
    This is a reminder that you have a trek assigned for {tomorrow}.\n
Trek Details:\n
    Trek Name: {trek.route.name}\n
    Location: {trek.route.location}\n
    Reporting Time: {trek.reporting_time}\n
Best regards,\nTrekOps Team"""
        send_email.delay(email, "Daily Reminder", body=body)

@shared_task
def monthly_report():
    today = date.today()
    first_day_current_month = today.replace(day=1)
    last_day_previous_month = first_day_current_month - timedelta(days=1)
    first_day_previous_month = last_day_previous_month.replace(day=1)
    treks = Trek.query.filter(Trek.start_date >= first_day_previous_month, Trek.start_date <= last_day_previous_month).all()
    no_of_treks = len(treks)
    no_of_participants = 0
    no_of_registered_trekkers = Trekker.query.count()
    no_of_registered_trekkers_previous_month =  Trekker.query.join(User).filter(
        User.create_datetime >= first_day_previous_month,
        User.create_datetime <= last_day_previous_month
    ).count()
    no_of_staff = Staff.query.count()
    active_staff = len([trek.staff for trek in treks])
    for trek in treks:
        no_of_participants += trek.total_slots - trek.available_slots
    popular_treks = []
    for trek in treks:
        trek_dict = {
            "name": trek.route.name,
            "location": trek.route.location,
            "occupancy": trek.total_slots - trek.available_slots/trek.total_slots * 100,
        }
        popular_treks.append(trek_dict)
    popular_treks = sorted(popular_treks, key=lambda x: x["occupancy"], reverse=True)[:5]
    report_html = render_template("monthly_report.html", month=first_day_previous_month.strftime("%B %Y"),
    no_of_treks=no_of_treks, no_of_participants=no_of_participants,
     no_of_registered_trekkers=no_of_registered_trekkers, 
     no_of_registered_trekkers_previous_month=no_of_registered_trekkers_previous_month, 
     no_of_staff=no_of_staff, active_staff=active_staff, popular_treks=popular_treks)
    send_email.delay("karanasvak@gmail.com", f"Monthly Report for {first_day_previous_month.strftime('%B %Y')}", html=report_html)

@shared_task
def export_history_csv(trekker_id):
    bookings = Bookings.query.filter(Bookings.trekker_id == trekker_id).all()
    os.makedirs("exports", exist_ok=True)

    filename = f"exports/history_{trekker_id}.csv"

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow([
            "User ID",
            "Trek Name",
            "Location",
            "Start Date",
            "End Date",
            "Status"
        ])

        for booking in bookings:
            writer.writerow([
                trekker_id,
                booking.trek.route.name,
                booking.trek.route.location,
                booking.trek.start_date.strftime("%d-%m-%Y"),
                booking.trek.end_date.strftime("%d-%m-%Y"),
                booking.status
            ])

    return filename



