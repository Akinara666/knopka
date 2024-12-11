from flask import Flask
from .auth import auth_bp
from .user import user_bp
from .movies import movies_bp

def register_blueprints(app: Flask):
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(movies_bp, url_prefix='/api/movies')
