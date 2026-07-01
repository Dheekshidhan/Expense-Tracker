from flask import Blueprint

# Create the dashboard blueprint with a dedicated url prefix
dashboard_bp = Blueprint('dashboard', __name__)

from app.dashboard import routes