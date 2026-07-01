from app import create_app
from app.extensions import db
from app.models import Category

app = create_app()

DEFAULT_CATEGORIES = [
    'Food', 'Transport', 'Rent', 'Utilities',
    'Entertainment', 'Shopping', 'Health', 'Other'
]

with app.app_context():
    db.create_all()  # Creates all tables based on models.py

    for name in DEFAULT_CATEGORIES:
        exists = Category.query.filter_by(name=name).first()
        if not exists:
            db.session.add(Category(name=name))

    db.session.commit()
    print("Database initialized and categories seeded successfully.")