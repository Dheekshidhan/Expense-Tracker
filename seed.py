from datetime import datetime, timedelta, timezone
from werkzeug.security import generate_password_hash
from app import create_app
from app.extensions import db
from app.models import Category, User, Expense

app = create_app()

DEFAULT_CATEGORIES = [
    'Food', 'Transport', 'Rent', 'Utilities',
    'Entertainment', 'Shopping', 'Health', 'Other'
]

with app.app_context():
    db.create_all()  # Creates all tables based on models.py

    # --- Seed categories ---
    for name in DEFAULT_CATEGORIES:
        exists = Category.query.filter_by(name=name).first()
        if not exists:
            db.session.add(Category(name=name))
    db.session.commit()

    # --- Seed a demo user (only if it doesn't already exist) ---
    demo_user = User.query.filter_by(email='demo@example.com').first()
    if not demo_user:
        demo_user = User(
            username='demo',
            email='demo@example.com',
            password_hash=generate_password_hash('demo123', method='pbkdf2:sha256')
        )
        db.session.add(demo_user)
        db.session.commit()
        print("Demo user created: demo@example.com / demo123")
    else:
        print("Demo user already exists, skipping creation.")

    # --- Seed sample expenses for the demo user (only if they have none yet) ---
    existing_expenses = Expense.query.filter_by(user_id=demo_user.id).count()
    if existing_expenses == 0:
        food = Category.query.filter_by(name='Food').first()
        transport = Category.query.filter_by(name='Transport').first()
        rent = Category.query.filter_by(name='Rent').first()
        entertainment = Category.query.filter_by(name='Entertainment').first()
        shopping = Category.query.filter_by(name='Shopping').first()

        sample_expenses = [
            Expense(amount=450.00, description='Groceries', category_id=food.id,
                    user_id=demo_user.id, date=datetime.now(timezone.utc) - timedelta(days=1)),
            Expense(amount=120.00, description='Auto ride', category_id=transport.id,
                    user_id=demo_user.id, date=datetime.now(timezone.utc) - timedelta(days=2)),
            Expense(amount=8000.00, description='Monthly rent', category_id=rent.id,
                    user_id=demo_user.id, date=datetime.now(timezone.utc) - timedelta(days=3)),
            Expense(amount=600.00, description='Movie night', category_id=entertainment.id,
                    user_id=demo_user.id, date=datetime.now(timezone.utc) - timedelta(days=4)),
            Expense(amount=1500.00, description='New shoes', category_id=shopping.id,
                    user_id=demo_user.id, date=datetime.now(timezone.utc) - timedelta(days=5)),
            Expense(amount=300.00, description='Restaurant dinner', category_id=food.id,
                    user_id=demo_user.id, date=datetime.now(timezone.utc) - timedelta(days=6)),
        ]

        db.session.add_all(sample_expenses)
        db.session.commit()
        print(f"Seeded {len(sample_expenses)} sample expenses for demo user.")
    else:
        print("Demo user already has expenses, skipping expense seeding.")

    print("Database initialization complete.")