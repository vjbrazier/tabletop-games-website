"""
The User Manager class. Manages Users, and saves/loads data to/from the JSON.
"""
# Standard Imports
import json

# Custom imports
from user import User
import core
from tabletop_logger import add_to_log

# Default statistics
default_game_stats = {
    'battleship': {
        'wins': 0,
        'losses': 0,
        'ratio': 0,
        'ships_sunk': 0,
        'shots_hit': 5,
        'shots_missed': 0,
        'total_shots': 0,
    },

    'blackjack': {
        'wins': 0,
        'losses': 0,
        'ratio': 0,
        'hits': 0,
    },

    'candyland': {
        'wins': 0,
        'losses': 0,
        'ratio': 0,
        'rainbow_trail': 0,
        'gumdrop_pass': 0,
        'gingerbread_men': 0,
        'gumdrops': 0,
        'candy_canes': 0,
        'peanuts': 0,
        'lollipops': 0,
        'ice_cream': 0,
        'licorice': 0,
        'spaces_moved': 0,
    },

    'catan': {
        'wins': 0,
        'losses': 0,
        'ratio': 0,
    },

    'chutes_and_ladders': {
        'wins': 0,
        'losses': 0,
        'ratio': 0,
        'chutes': 0,
        'ladders': 0,
    },

    'clue': {
        'wins': 0,
        'losses': 0,
        'ratio': 0,
    },

    'connect_four': {
        'wins': 0,
        'losses': 0,
        'ratio': 0,
        'red_pieces': 0,
        'yellow_pieces': 0,
        'total_pieces': 0,
    },

    'monopoly': {
        'wins': 0,
        'losses': 0,
        'ratio': 0,
    },

    'sorry': {
        'wins': 0,
        'losses': 0,
        'ratio': 0,
        'sorrys': 0,
        'swaps': 0,
    },

    'uno': {
        'wins': 0,
        'losses': 0,
        'ratio': 0,
        'unos': 0,
        'total_drawn': 0,
    }
}

class UserManager:
    """
    Class used to handle users.
    """
    def __init__(self, user_data_path=core.user_data_path):
        self.user_data_path = user_data_path
        self.users = self.load_users()

        self.add_missing_data()
        self.remove_deleted_data()
        self.sort_games()
        self.sort_game_stats()
        self.save_users()

    def load_users(self):
        """
        Loads users from the JSON into live memory using the User class.
        """
        with open(self.user_data_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)

        users = {}

        for username, data in raw_data.items():
            add_to_log(f'[INFO] Loading data for {username}...')

            users[username] = User(
                username=username,
                password=data.get('password'),
                wins=data.get('wins'),
                losses=data.get('losses'),
                ratio=data.get('ratio'),
                game_stats=data.get('game_stats')
            )

            add_to_log(f'[INFO] Finished loading data for {username}.')

        add_to_log('[INFO] Successfully loaded all users!')
        return users

    def create_user(self, username, password):
        """
        Creates a user with the username and password given.
        """
        add_to_log(f'[INFO] Creating user {username}...')
        self.users[username] = User(username=username, password=password)
        self.add_missing_data()
        add_to_log(f'[INFO] Finished creating {username}!')
        self.save_users()

    def save_users(self):
        """
        Saves users to the JSON file.
        """
        add_to_log('[INFO] Saving current User data...')
        with open(self.user_data_path, 'w', encoding='utf-8') as f:
            json.dump({user.username: user.to_dict() for user in self.users.values()}, f, indent=4)
        add_to_log('[INFO] Finished saving User data!')


    def remove_deleted_data(self):
        """
        Removes data that has been deleted.
        """
        users = self.users.values()

        for user in users:
            add_to_log(f'[INFO] Removing deleted game data for {user.get_username()}...')
            user.game_stats = {
                game: stats for game, stats in user.game_stats.items()
                if game in default_game_stats
            }

            add_to_log(f'[INFO] Removing deleted game stats for {user.get_username()}...')
            for game in user.game_stats:
                existing_stats = default_game_stats.get(game)
                user.game_stats[game] = {
                    stat: value for stat, value in user.game_stats.get(game).items()
                    if stat in existing_stats
                }
            
            add_to_log(f'[INFO] Finished removing deleted data for {user.get_username()}!')
        
        add_to_log('[INFO] Finished removing deleted data for all users!')

    def add_missing_data(self):
        """
        Adds data missing from the User.
        """
        users = self.users.values()

        for user in users:
            add_to_log(f'[INFO] Adding missing games and game stats for {user.get_username()}...')
            for game, stats in default_game_stats.items():
                user.game_stats.setdefault(game, stats.copy())

                for stat in stats:
                    user.game_stats[game].setdefault(stat, 0)

            add_to_log(f'[INFO] Finished adding missing games and game stats for {user.get_username()}!')

        add_to_log('[INFO] Finished adding missing games and game stats for all users!')

    def sort_games(self):
        """
        Alphabetically sorts the games in game_stats
        """
        users = self.users.values()
        game_order = sorted(default_game_stats.keys())

        for user in users:
            add_to_log(f'[INFO] Sorting games for {user.get_username()}...')
            user.game_stats = {
                game: user.game_stats.get(game) for game in game_order
            }
            add_to_log(f'[INFO] Finished sorting games for {user.get_username()}!')

        add_to_log('[INFO] Finished sorting games for all users!')

    def sort_game_stats(self):
        """
        Sorts game stats (note: sorted how I like, not alphabetical or anything)
        """
        users = self.users.values()

        for user in users:
            add_to_log(f'[INFO] Sorting game stats for {user.get_username()}')
            for game, stat_order in default_game_stats.items():
                user.game_stats[game] = {
                    stat: user.game_stats[game][stat] for stat in stat_order
                }
            add_to_log(f'[INFO] Finished sorting game stats for {user.get_username()}!')

        add_to_log('[INFO] Finished sorting game stats for all users!')
