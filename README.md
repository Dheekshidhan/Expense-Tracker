# Expense Tracker

A full-stack expense tracking web application built with Flask, featuring user authentication, category-based expense management, a live spending visualization, and a REST API endpoint.

**Live demo:** https://expense-tracker-zs84.onrender.com
*(Free-tier hosting — the app may take ~30-60 seconds to wake up on first load if it's been idle.)*

**Demo login:**
- Email: `demo@example.com`
- Password: `demo123`

## Features

- **User authentication** — registration and login with secure password hashing (`pbkdf2:sha256` via Werkzeug), session management via Flask-Login
- **Expense CRUD** — add and delete expenses, each tied to a category and the logged-in user
- **Ownership enforcement** — users can only view/delete their own expenses, verified server-side on every request
- **Dashboard** — total spend, transaction count, and a full expense history table
- **Spending visualization** — a doughnut chart (Chart.js) breaking down spend by category, powered by a client-side fetch call to the app's own API
- **REST API** — a JSON endpoint (`/api/summary`) returning structured expense data, independent of the HTML views
- **CSRF protection** — all state-changing forms (register, login, add/delete expense) are protected via Flask-WTF's `CSRFProtect`

## Tech Stack

- **Backend:** Python, Flask
- **Database:** SQLite via Flask-SQLAlchemy (ORM)
- **Auth:** Flask-Login, Werkzeug password hashing
- **Security:** Flask-WTF (CSRF protection)
- **Frontend:** Jinja2 templates, vanilla CSS, Chart.js (via CDN)
- **Deployment:** Render (Gunicorn as the production WSGI server)

## Architecture

The app follows Flask's **application factory** pattern with **blueprints**, separating concerns into independent modules:

```
app/
├── auth/        → registration, login, logout
├── expenses/    → add/delete expense logic
├── dashboard/   → main view, aggregates + renders expense data
├── api/         → JSON endpoint for programmatic access
├── models.py    → User, Category, Expense (SQLAlchemy models)
└── extensions.py → shared db/login/csrf objects (avoids circular imports)
```

This structure was a deliberate choice over a single-file app — it mirrors how production Flask apps are typically organized and keeps each feature area independently testable and extendable.

## Running Locally

1. Clone the repo:
   ```
   git clone https://github.com/Dheekshidhan/expense-tracker.git
   cd expense-tracker
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root:
   ```
   SECRET_KEY=your-own-random-secret-key
   ```

4. Initialize the database (creates tables, seeds default categories, and a demo user):
   ```
   python seed.py
   ```

5. Run the app:
   ```
   python run.py
   ```
   Visit `http://127.0.0.1:5000`

## Known Limitations

- Uses SQLite, which is fine for development/demo purposes but isn't ideal for concurrent production use — the `SQLALCHEMY_DATABASE_URI` is environment-configurable, so swapping to PostgreSQL is a one-line change if needed.
- Deployed on Render's free tier, which has an ephemeral filesystem — the database resets on redeploys/restarts. Not an issue for this project's purpose as a portfolio demo.

## Author

Built by Dheekshidhan as a portfolio project.
