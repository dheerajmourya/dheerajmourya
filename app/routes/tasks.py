from flask import Blueprint, request, jsonify
from app.models import db, Task, TaskDependency, User, Project
from app.utils.validators import is_circular_dependency
from app.utils.auth import token_required

tasks_bp = Blueprint('tasks', __name__)

# 1. Create Task under a Project (✅ Secured)
@tasks_bp.route('/projects/<int:project_id>/tasks', methods=['POST'])
@token_required
def create_task(user_id, project_id):
    data = request.get_json()

    title = data.get('title')
    assigned_user_id = data.get('user_id')  # Note: this is who the task is assigned to
    dependencies = data.get('dependencies', [])

    if not title or not assigned_user_id:
        return jsonify({'error': 'Title and user_id are required'}), 400

    user = User.query.get(assigned_user_id)
    if not user:
        return jsonify({'error': 'Assigned user not found'}), 404

    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404

    try:
        task = Task(title=title, status='pending', user_id=assigned_user_id, project_id=project_id)
        db.session.add(task)
        db.session.flush()  # get task.id without commit

        # Add dependencies if any
        for dep_id in dependencies:
            dep_task = Task.query.get(dep_id)
            if not dep_task:
                db.session.rollback()
                return jsonify({'error': f"Dependency task {dep_id} not found"}), 400

            if is_circular_dependency(task.id, dep_id):
                db.session.rollback()
                return jsonify({'error': 'Circular dependency detected'}), 400

            td = TaskDependency(task_id=task.id, depends_on_id=dep_id)
            db.session.add(td)

        db.session.commit()
        return jsonify({'id': task.id, 'title': task.title, 'status': task.status}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# 2. Get Task by ID (✅ Secured)
@tasks_bp.route('/tasks/<int:task_id>', methods=['GET'])
@token_required
def get_task(user_id, task_id):
    task = Task.query.get_or_404(task_id)
    return jsonify({
        'id': task.id,
        'title': task.title,
        'status': task.status,
        'user_id': task.user_id,
        'project_id': task.project_id,
        'dependencies': [d.id for d in task.dependencies]
    }), 200

# 3. Update Task Status (✅ Secured)
@tasks_bp.route('/tasks/<int:task_id>/status', methods=['PATCH'])
@token_required
def update_task_status(user_id, task_id):
    data = request.get_json()
    new_status = data.get('status')

    if new_status not in ['pending', 'in-progress', 'completed']:
        return jsonify({'error': 'Invalid status'}), 400

    task = Task.query.get_or_404(task_id)

    if new_status == 'completed':
        for dep in task.dependencies:
            if dep.status != 'completed':
                return jsonify({'error': 'All dependencies must be completed before marking this task completed'}), 400

    try:
        task.status = new_status
        db.session.commit()
        return jsonify({'message': 'Status updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# 4. List tasks assigned to a user (✅ Secured)
@tasks_bp.route('/users/<int:target_user_id>/tasks', methods=['GET'])
@token_required
def get_tasks_for_user(user_id, target_user_id):
    user = User.query.get_or_404(target_user_id)
    tasks = Task.query.filter_by(user_id=user.id).all()
    return jsonify([
        {'id': t.id, 'title': t.title, 'status': t.status}
        for t in tasks
    ]), 200

# 5. List tasks by status (✅ Secured)
@tasks_bp.route('/tasks', methods=['GET'])
@token_required
def list_tasks_by_status(user_id):
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    status = request.args.get('status')

    query = Task.query
    if status:
        if status not in ['pending', 'in-progress', 'completed']:
            return jsonify({'error': 'Invalid status'}), 400
        query = query.filter_by(status=status)

    tasks_query = query.paginate(page=page, per_page=limit, error_out=False)
    tasks = tasks_query.items

    return jsonify({
        'tasks': [{'id': t.id, 'title': t.title, 'status': t.status} for t in tasks],
        'total': tasks_query.total,
        'page': page,
        'pages': tasks_query.pages
    }), 200
