from datetime import datetime
from flask_login import UserMixin
from app.extensions import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    """Flask-Login helper to fetch a user from the database by their ID."""
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships: Links the user to their expenses
    expenses = db.relationship('Expense', backref='author', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User '{self.username}'>"


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    # Relationship: Links category to expenses
    expenses = db.relationship('Expense', backref='category', lazy=True)

    def __repr__(self):
        return f"<Category '{self.name}'>"


class Expense(db.Model):
    __tablename__ = 'expenses'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)

    # Foreign Keys: Connecting this expense to a specific User and Category
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

    def __repr__(self):
        return f"<Expense {self.amount} - {self.date.strftime('%Y-%m-%d')}>"