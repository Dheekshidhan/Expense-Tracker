from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.expenses import expenses_bp
from app.models import Expense, Category
from app.extensions import db


@expenses_bp.route('/expense/add', methods=['GET', 'POST'])
@login_required
def add_expense():
    """Handles adding a new transaction."""
    # Fetch all categories from the DB so the user can select one in a dropdown menu
    categories = Category.query.all()

    if request.method == 'POST':
        amount = request.form.get('amount')
        description = request.form.get('description')
        category_id = request.form.get('category_id')

        if not amount or not category_id:
            flash('Amount and Category are required!', 'danger')
            return redirect(url_for('expenses.add_expense'))

        new_expense = Expense(
            amount=float(amount),
            description=description,
            category_id=int(category_id),
            user_id=current_user.id
        )

        db.session.add(new_expense)
        db.session.commit()
        flash('Expense added successfully!', 'success')
        return redirect(url_for('dashboard.index'))

    return render_template('expenses/add_expense.html', categories=categories)


@expenses_bp.route('/expense/delete/<int:expense_id>', methods=['POST'])
@login_required
def delete_expense(expense_id):
    """Safely deletes an expense item."""
    expense = Expense.query.get_or_404(expense_id)

    # Security check: Ensure the logged-in user actually owns this specific expense entry!
    if expense.user_id != current_user.id:
        flash('You do not have permission to delete this entry.', 'danger')
        return redirect(url_for('dashboard.index'))

    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted.', 'info')
    return redirect(url_for('dashboard.index'))