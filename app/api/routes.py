from flask import jsonify
from flask_login import login_required, current_user
from app.api import api_bp
from app.models import Expense


@api_bp.route('/summary', methods=['GET'])
@login_required
def get_expense_summary():
    """Returns the logged-in user's spending data structured in clean JSON format."""
    user_expenses = Expense.query.filter_by(user_id=current_user.id).all()

    # Structure data into a raw list of dictionaries
    data = []
    for exp in user_expenses:
        data.append({
            'id': exp.id,
            'amount': exp.amount,
            'description': exp.description,
            'date': exp.date.strftime('%Y-%m-%d'),
            'category': exp.category.name if exp.category else 'Uncategorized'
        })

    # Return data as a machine-readable JSON array
    return jsonify({
        'status': 'success',
        'total_count': len(data),
        'total_spent': sum(exp.amount for exp in user_expenses),
        'expenses': data
    })