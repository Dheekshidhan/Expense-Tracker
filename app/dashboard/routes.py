from flask import render_template
from flask_login import login_required, current_user
from app.dashboard import dashboard_bp
from app.models import Expense
from app.extensions import db


@dashboard_bp.route('/')
@login_required
def index():
    """Fetches user-specific expense data and displays the dashboard dashboard."""
    # Fetch all expenses belonging ONLY to the logged-in user, ordered by newest first
    user_expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.date.desc()).all()

    # Calculate quick mathematical metrics for the UI dashboard
    total_spent = sum(expense.amount for expense in user_expenses)
    total_transactions = len(user_expenses)

    return render_template(
        'dashboard/index.html',
        expenses=user_expenses,
        total_spent=total_spent,
        total_transactions=total_transactions
    )