from flask import Blueprint, request, jsonify
from app.models import db, Project
from app.utils.auth import token_required

projects_bp = Blueprint('projects', __name__)

# ✅ SECURED: Create new project
@projects_bp.route('/projects', methods=['POST'])
@token_required
def create_project(user_id):
    data = request.get_json()
    project = Project(name=data['name'], description=data.get('description'))
    db.session.add(project)
    db.session.commit()
    return jsonify({'id': project.id, 'name': project.name}), 201

# ✅ SECURED: List all projects with pagination
@projects_bp.route('/projects', methods=['GET'])
@token_required
def list_projects(user_id):
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)

    projects_query = Project.query.paginate(page=page, per_page=limit, error_out=False)
    projects = projects_query.items

    return jsonify({
        'projects': [{'id': p.id, 'name': p.name} for p in projects],
        'total': projects_query.total,
        'page': page,
        'pages': projects_query.pages
    }), 200

# ✅ Optional: Public project detail (can leave open or secure as per use-case)
@projects_bp.route('/projects/<int:project_id>', methods=['GET'])
@token_required
def get_project(user_id, project_id):
    project = Project.query.get_or_404(project_id)
    return jsonify({'id': project.id, 'name': project.name, 'description': project.description}), 200

# ✅ SECURED: Get tasks for a specific project
@projects_bp.route('/projects/<int:project_id>/tasks', methods=['GET'])
@token_required
def get_project_tasks(user_id, project_id):
    project = Project.query.get_or_404(project_id)
    return jsonify([
        {'id': t.id, 'title': t.title, 'status': t.status}
        for t in project.tasks
    ]), 200
