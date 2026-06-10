from urllib.parse import quote_plus

class Config:
    SECRET_KEY = 'mentorlink_secret_key_2026'
    
    raw_password = 'password7640'
    
    encoded_password = quote_plus(raw_password)
    SQLALCHEMY_DATABASE_URI = f'postgresql://postgres:{encoded_password}@localhost:5432/mentorlink'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {
            "options": "-c client_encoding=utf8"
        }
    }