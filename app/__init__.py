from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO
from config import Config

db      = SQLAlchemy()
bcrypt  = Bcrypt()
login_manager = LoginManager()
socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)

    login_manager.login_view = 'auth.connexion'

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes.auth       import auth
    from app.routes.profil     import profil
    from app.routes.matching   import matching
    from app.routes.messagerie import messagerie
    from app.routes.agenda     import agenda

    app.register_blueprint(auth)
    app.register_blueprint(profil)
    app.register_blueprint(matching)
    app.register_blueprint(messagerie)
    app.register_blueprint(agenda)

    return app
