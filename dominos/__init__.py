import eventlet
# Eventlet isn't compatible with some python modules (e.g. time) so monkeypatch to resolve
# bugs that result from such conflicts
eventlet.monkey_patch()
from flask import Flask
from flask_socketio import SocketIO
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from AppConfig import AppConfig

app = Flask(__name__)
# app.config.from_object(AppConfig)
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
socketio = SocketIO(app, cors_allowed_origins="*")

# Import relevant flask handling modules here, to avoid circular imports
from dominos import socketio_handlers#, models

