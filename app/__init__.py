from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    from app.routes import main 
    #from app.test_routes import main
    
    from app.auth_routes import auth

    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app