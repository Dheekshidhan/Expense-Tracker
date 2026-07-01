from flask import Blueprint

# Create the authentication blueprint
auth_bp = Blueprint('auth', __name__)

# Import the routes so Flask knows they exist under this blueprint
from app.auth import routes