import os
from dotenv import load_dotenv

# Load variables from .env file into the environment
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Secret key used by Flask for sessions, CSRF protection, etc.
    SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-dev-key-change-this')

    # Database location — SQLite file stored in instance/ folder
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///' + os.path.join(basedir, 'instance', 'expense_tracker.db')
    )

    # Disables a feature we don't need, saves memory
    SQLALCHEMY_TRACK_MODIFICATIONS = False