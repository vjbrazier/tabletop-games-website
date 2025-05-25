"""
Contains the routes to the various pages on the site.
"""
# Third-party imports
from flask import render_template, redirect, url_for

# Custom imports
from core import app

@app.route('/')
def index():
    """
    The main page of the website.
    """
    return render_template('index.html')
