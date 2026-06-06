class Config:
    SECRET_KEY = 'mentorlink_secret_key'
    SQLALCHEMY_DATABASE_URI = 'mysql:root:@localhost/mentorlink_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False