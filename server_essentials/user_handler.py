"""
Allows for logging in, and has various functions for the user data.

"""
# Standard Imports
import json

# Third party imports
from flask import render_template, request, redirect,  url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

# Custom imports
import core

login_manager = LoginManager()
login_manager.init_app(core.app)

# Default statistics
# Stats that are independent of games
universal_stats = ['wins', 'losses', 'ratio'] 

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
    def __init__(self, username, stats):
        self.username = username
        self.stats = stats