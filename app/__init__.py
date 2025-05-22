from flask import Flask
from app.models import db
from app.routes.users import users_bp
from app.routes.projects import projects_bp
from app.routes.tasks import tasks_bp
from app.routes.auth import auth_bp

def create_app():
    app = Flask(__name__)

    # DB config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/task_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Register blueprints
    app.register_blueprint(users_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()

    return app
