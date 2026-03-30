from app import app, init_db

# Initialize MongoDB when Gunicorn loads the app
db_available = init_db()
app.config['DB_AVAILABLE'] = db_available

# Expose `app` for Gunicorn
# Gunicorn command: gunicorn wsgi:app
