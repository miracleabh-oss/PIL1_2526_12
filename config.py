class Config:
    SECRET_KEY = 'mentorlink_secret_key_2026'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password7640@localhost:5432/mentorlink'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {
            "options": "-c client_encoding=utf8"
        }
    }
