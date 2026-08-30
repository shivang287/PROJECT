"""Flask application factory."""
from flask import Flask, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.__init__(app)

    from app.routes.auth import auth_bp
    from app.routes.tasks import tasks_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)

    # Home route
    @app.route('/')
    def home():
        if 'user' in session:
            return redirect(url_for('tasks.view_tasks'))
        return redirect(url_for('auth.login'))

    return app
