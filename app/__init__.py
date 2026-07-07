from flask import Flask
from config import Config
from app.extensions import db, login_manager, migrate, csrf


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Attach our extensions to this specific app instance
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # Tell Flask-Login where to redirect if someone tries to
    # access a protected page without being logged in
    login_manager.login_view = 'auth.login'

    # Register blueprints (each feature area's routes)
    from app.auth.routes import auth_bp
    from app.expenses.routes import expenses_bp
    from app.dashboard.routes import dashboard_bp
    from app.api.routes import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(expenses_bp)
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(api_bp, url_prefix='/api')
    from flask import redirect, url_for
    from flask_login import current_user

    @app.route('/')
    def root():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard.index'))
        return redirect(url_for('auth.login'))
    return app