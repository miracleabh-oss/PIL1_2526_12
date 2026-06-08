from flask import Flask 
from config import Config 

def create_app():
    app = Flask (__name__)
    app.config.from_object(Config)

    from app.routes.auth import auth
    from app.routes.profil import profil
    from app.routes.matching import matching
    from app.routes.messagerie import messagerie
    
    app.register_blueprint(auth)
    app.register_blueprint(profil)
    app.register_blueprint(matching)
    app.register_blueprint(messagerie)

    return app
