"""
Contains the routes to the various pages on the site.
"""
# Third-party imports
from flask import render_template, redirect, url_for

# Custom imports
from core import app
from user_manager import default_game_stats

games = default_game_stats.keys()

@app.route('/')
def index():
    """
    The index page of the website.
    """
    return render_template('index.html', page_id='index', page_title='Tabletop Games - Index', games=games)
