from app import create_app
from app.models import db, User, Project, Task, TaskDependency

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # Create Users
    u1 = User(name='Alice', email='alice@example.com')
    u2 = User(name='Bob', email='bob@example.com')
    db.session.add_all([u1, u2])
    db.session.flush()  # Get IDs without committing

    # Create Project
    p1 = Project(name='Demo Project', description='This is a demo project.')
    db.session.add(p1)
    db.session.flush()

    # Create Tasks
    t1 = Task(title='Setup Repo', status='completed', user_id=u1.id, project_id=p1.id)
    t2 = Task(title='Create DB Models', status='in-progress', user_id=u1.id, project_id=p1.id)
    t3 = Task(title='Build API', status='pending', user_id=u2.id, project_id=p1.id)
    db.session.add_all([t1, t2, t3])
    db.session.flush()

    # Add dependency: t3 depends on t2
    dep = TaskDependency(task_id=t3.id, depends_on_id=t2.id)
    db.session.add(dep)

    db.session.commit()
    print("✅ Seed data inserted successfully.")
