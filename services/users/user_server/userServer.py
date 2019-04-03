from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(script_info=None):

    app = Flask(__name__)

    app_settings = os.environ.get('APP_SETTINGS')
    app.config.from_object(app_settings)

    db.init_app(app)

    from user_server.api.users import users_blueprint
    app.register_blueprint(users_blueprint)

    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app
