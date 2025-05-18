"""
The User Manager class. Manages Users, and saves/loads data to/from the JSON.

"""
# Standard Imports
import json
import sys
import os

# Third party imports
from flask import render_template, request, redirect,  url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

# Custom imports
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from user import User
import core

login_manager = LoginManager()
login_manager.init_app(core.app)

# Default statistics
# Stats that are independent of games
global_stats = ['wins', 'losses', 'ratio']

# The default order of player traits
player_traits_order = {'password': None,
                       'wins': None, 
                       'losses': None, 
                       'ratio': None, 
                       'game_specific': None
                       }

# Stats that are tied to specific games
default_game_stats = {
    "battleship": {
        "wins": 0,
        "losses": 0,
        "ratio": 0,
        "ships_sunk": 0,
        "shots_hit": 0,
        "shots_missed": 0,
        "total_shots": 0,
    },

    "blackjack": {
        "wins": 0,
        "losses": 0,
        "ratio": 0,
        "hits": 0,
    },

    "candyland": {
        "wins": 0,
        "losses": 0,
        "ratio": 0,
        "rainbow_trail": 0,
        "gumdrop_pass": 0,
        "gingerbread_men": 0,
        "gumdrops": 0,
        "candy_canes": 0,
        "peanuts": 0,
        "lollipops": 0,
        "ice_cream": 0,
        "licorice": 0,
        "spaces_moved": 0,
    },

    "catan": {
        "wins": 0,
        "losses": 0,
        "ratio": 0,
    },

    "chutes_and_ladders": {
        "wins": 0,
        "losses": 0,
        "ratio": 0,
        "chutes": 0,
        "ladders": 0,
    },

    "clue": {
        "wins": 0,
        "losses": 0,
        "ratio": 0,
    },

    "connect_four": {
        "wins": 0,
        "losses": 0,
        "ratio": 0,
        "red_pieces": 0,
        "yellow_pieces": 0,
        "total_pieces": 0,
    },

    "monopoly": {
        "wins": 0,
        "losses": 0,
        "ratio": 0,
    },

    "sorry": {
        "wins": 0,
        "losses": 0,
        "ratio": 0,
        "sorrys": 0,
        "swaps": 0,
    },

    "uno": {
        "wins": 0,
        "losses": 0,
        "ratio": 0,
        "unos": 0,
        "total_drawn": 0,
    }
}

class UserManager:
    """
    Class used to handle users
    """
    def __init__(self, user_data_path=core.user_data_path):
        self.user_data_path = user_data_path
        self.users = self.load_users()

        self.add_missing_data()
        # self.sort_data()
        # self.save_users()

    def load_users(self):
        """
        Loads users from the JSON into live memory using the User class.
        """
        with open(self.user_data_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)

        users = {}

        for username, data in raw_data.items():
            users[username] = User(
                username=username,
                password=data.get('password'),
                wins=data.get('wins'),
                losses=data.get('losses'),
                ratio=data.get('ratio'),
                game_stats=data.get('game_stats')
            )

        return users

    def create_user(self, username, password):
        self.users[username] = User(username=username, password=password)
        self.add_missing_data()

    def save_users(self):
        """
        Saves users to the JSON file.
        """
        with open(self.user_data_path, 'w', encoding='utf-8') as f:
            json.dump({user.to_dict() for user in self.users.values()}, f, indent=4)

    def add_missing_data(self):
        """
        Adds data missing from the User.
        Note: This is just game data, as the other data is initialized automatically.
        """
        for user in self.users.values():
            for game in default_game_stats:
                if not user.game_stats.get(game):
                    user.game_stats.setdefault(game, default_game_stats.get(game))

        self.save_users()
