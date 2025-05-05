"""
This module runs the server.
"""
# Standard imports
import importlib
import os
import json
from pathlib import Path

# Custom imports
import core

def load_folder(folder):
    """
    Loads all the python files in a folder automatically.
        folder: the folder to load
    """

    for filename in os.listdir(folder):
        # Prevents loading unneeded files/init folders
        if filename.endswith('.py') and filename != '__init__.py':

            # Grabs by name without the extension
            module_name = f'{folder}.{filename[:-3]}'
            importlib.import_module(module_name)

load_folder(Path('server_essentials'))
load_folder(Path('socketio_listeners'))

if __name__ == '__main__':
    # Loads up the list of users
    with open (core.data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Adds missing data, reorders unordered data
    # for user in data:
    #     load_specific_user(user, False)

    core.socketio.run(core.app, host='0.0.0.0', port=5000, debug=True)
