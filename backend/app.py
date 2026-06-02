from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mentorlink_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/mentorlink'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
socketio = SocketIO(app)

@app.route('/')
def accueil():
    return "MentorLink fonctionne !"

if __name__ == '__main__':
    socketio.run(app, debug=True)