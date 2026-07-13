import os
from celery.schedules import crontab

class Config:
    # Generate a nice key using secrets.token_urlsafe()
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw"
    )
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", "uploads")
    DEBUG = False
    
    # Generate a good salt using:
    # secrets.SystemRandom().getrandbits(128)
    SECURITY_PASSWORD_SALT = os.environ.get(
        "SECURITY_PASSWORD_SALT",
        "146585145368132386173505678016728509634"
    )

    # In-memory SQLite database
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///model.db"
    )

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False


    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "karanasvak@gmail.com"
    MAIL_PASSWORD = "rdhx lbte djbz zvtg"
    MAIL_DEFAULT_SENDER = "karanasvak@gmail.com"

    CELERY = {
    "broker_url": "redis://localhost:6379/0",
    "result_backend": "redis://localhost:6379/1",
    "timezone": "Asia/Kolkata",

    "beat_schedule": {
        "daily-reminder": {
            "task": "dep.tasks.send_daily_remainders",
            "schedule": crontab(hour="21", minute="0")
        },
        "monthly-report": {
            "task": "dep.tasks.monthly_report",
            "schedule": crontab(hour="8", minute="0", day_of_month="1")
        }
    },
}

    CACHE_TYPE="RedisCache"
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 2