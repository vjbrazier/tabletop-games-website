"""
The User class. Handles data related to the User, and allows creation of Users
"""
from flask_login import UserMixin

class User(UserMixin):
    """
    User class. Creates instances of users.

    Parameters: username, password, wins, losses, ratio, game_stats.
    """
    def __init__(self, username, password='', wins=0, losses=0, ratio=0, game_stats=None):
        if game_stats is None:
            game_stats = {}

        self.username = username
        self.password = password
        self.wins = wins
        self.losses = losses
        self.ratio = ratio
        self.game_stats = game_stats

    def get_username(self):
        return self.username

    def set_stat(self, stat, value=0, increment=True, game=None):
        """
        Sets a stat based on the value given. 

        increment: used to determine if the stat should be increased by one.
        game: used to determine if it is a global or nested stat.
        """
        if increment:
            if value == 0:
                value = 1
            else:
                value += 1

        if game is None:
            setattr(self, stat, value)

        else:
            self.game_stats.setdefault(game, {})[stat] = value

    def get_stat(self, stat, game=None):
        """
        Gets the value of a stat.

        game: used to determine if it is a global or nested stat.
        """
        if game is None:
            return getattr(self, stat, 0)

        else:
            return self.game_stats.get(game, {}).get(stat, 0)

    def ratio_validity_check(self, wins, losses):
        """
        Returns the ratio. Adjusts it based on any 0s present.
        """
        if wins == 0 and losses != 0:
            return -losses
        elif losses == 0:
            return wins
        else:
            return wins / losses

    def determine_stat_changes(self, stat, game=None):
        """
        Identifies what stats need to be modified, before setting it.
        """
        if stat in ['wins', 'losses']:
            self.set_stat(stat, self.get_stat(stat, None))

            global_ratio = self.ratio_validity_check(self.get_stat('wins'), self.get_stat('losses'))

            self.set_stat('ratio', global_ratio, False)

            if game is not None:
                game_ratio = self.ratio_validity_check(self.get_stat('wins', game), self.get_stat('losses', game))

                self.set_stat('ratio', game_ratio, False, game)

        else:
            self.set_stat(stat, self.get_stat(stat, game), game)

    def to_dict(self):
        """
        Returns the User as a dictionary.
        """
        return {
                'password': self.password,
                'wins': self.wins,
                'losses': self.losses,
                'ratio': self.ratio,
                'game_stats': self.game_stats
               }
