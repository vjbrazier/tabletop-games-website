"""
This module contains variables and objects shared across the project.
"""
# Standard imports
from pathlib import Path

# Third party imports
from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)
app.secret_key = 'placeholder'

data_path = Path('data/users.json')
