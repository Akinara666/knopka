from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from config import Config
from models import db
from blueprints import register_blueprints


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    CORS(app)
    Migrate(app, db)

    # Register blueprints
    register_blueprints(app)

    return app

app = create_app(config_class=Config)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
