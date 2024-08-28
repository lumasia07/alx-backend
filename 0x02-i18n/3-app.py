#!/usr/bin/env python3
"""Basic Flask Babel setup with locale selection"""
from flask import Flask, render_template, request
from flask_babel import Babel, _

app = Flask(__name__)

class Config:
    """Basic config"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"

app.config.from_object(Config)

babel = Babel(app)

@babel.localeselector
def get_locale():
    """Find best match"""
    return request.accept_languages.best_match(app.config['LANGUAGES'])

@app.route('/')
def index():
    """Index page"""
    return render_template('3-index.html', title=_("home_title"), header=_("home_header"))

if __name__ == "__main__":
    app.run(debug=True)
