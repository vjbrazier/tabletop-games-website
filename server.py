"""
This module runs the server.
"""
# Standard imports
import importlib
import os
from pathlib import Path

# Custom imports
import core
from user_manager import UserManager

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
    manager = UserManager()
    # manager.create_user("Vincent", "placeholder")
    # print(manager.users['Vincent'].to_dict())

    core.socketio.run(core.app, host='0.0.0.0', port=5000, debug=True)
