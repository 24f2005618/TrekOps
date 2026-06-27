import os


class Config:
    # Generate a nice key using secrets.token_urlsafe()
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw"
    )

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