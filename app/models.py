from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import CheckConstraint

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    tasks = db.relationship('Task', backref='assigned_user')

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    tasks = db.relationship('Task', backref='project')

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, in-progress, completed
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

    dependencies = db.relationship(
        'Task',
        secondary='task_dependencies',
        primaryjoin='Task.id==TaskDependency.task_id',
        secondaryjoin='Task.id==TaskDependency.depends_on_id',
        backref='dependent_tasks'
    )

class TaskDependency(db.Model):
    __tablename__ = 'task_dependencies'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    depends_on_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('task_id', 'depends_on_id', name='unique_dependency'),
    )
