#!/usr/bin/env python3
"""Mock user login"""
from flask import Flask, request, g, render_template
from flask_babel import Babel, _

app = Flask(__name__)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'fr']

babel = Babel(app)

@babel.localeselector
def get_locale():
    """Get locale"""
    locale = request.args.get('locale')
    if locale and locale in app.config['BABEL_SUPPORTED_LOCALES']:
        return locale
    
    if g.user and g.user.get('locale') in app.config['BABEL_SUPPORTED_LOCALES']:
        return g.user['locale']
    
    return request.accept_languages.best_match(app.config['BABEL_SUPPORTED_LOCALES'])

def get_user():
    """Retrieve a user based on the login_as param"""
    try:
        user_id = int(request.args.get('login_as'))
        return users.get(user_id)
    except (TypeError, ValueError):
        return None


@app.before_request
def before_request():
    """Set the user in the global g object before each request"""
    g.user = get_user()


@app.route('/')
def index():
    """Render template"""
    return render_template('5-index.html')


if __name__ == '__main__':
    app.run(debug=True)
