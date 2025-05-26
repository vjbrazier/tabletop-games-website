"""
This module contains variables and objects shared across the project.
"""
# Standard imports
from pathlib import Path
import os

# Third party imports
from flask import Flask
from flask_socketio import SocketIO

# Custom imports
from tabletop_logger import add_to_log

# Flask and SocketIO
app = Flask(__name__)
socketio = SocketIO(app)
app.secret_key = 'placeholder'

# Log paths
logs_folder_path = Path('logs/')

# User data paths
data_folder_path = Path('data/')
user_data_path = Path('data/users.json')

# Creating missing folders/files
if not os.path.exists(logs_folder_path):
    os.makedirs(logs_folder_path)
    add_to_log('[INFO] Created log folder.')

if not os.path.exists(data_folder_path):
    os.makedirs(Path('data/'))
    add_to_log('[INFO] Created data folder.')

if not os.path.exists(user_data_path):
    with open(user_data_path, 'w', encoding='utf-8') as f:
        f.write('{}')
        add_to_log('[INFO] Created user data file.')
