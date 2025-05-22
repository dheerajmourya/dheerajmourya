from flask import Blueprint, request, jsonify
from app.models import db, User
import re
from app.utils.auth import token_required

users_bp = Blueprint('users', __name__)

# ✅ PUBLIC Route (no token)
@users_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data.get('email') or not re.match(r"[^@]+@[^@]+\.[^@]+", data['email']):
        return jsonify({'error': 'Invalid email'}), 400

    user = User(name=data['name'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'id': user.id, 'name': user.name}), 201

# ✅ SECURED: List all users
@users_bp.route('/users', methods=['GET'])
@token_required
def list_users(user_id):
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)

    users_query = User.query.paginate(page=page, per_page=limit, error_out=False)
    users = users_query.items

    return jsonify({
        'users': [{'id': u.id, 'name': u.name, 'email': u.email} for u in users],
        'total': users_query.total,
        'page': page,
        'pages': users_query.pages
    }), 200

# ✅ SECURED: Get specific user
@users_bp.route('/users/<int:id>', methods=['GET'])
@token_required
def get_user(user_id, id):
    user = User.query.get_or_404(id)
    return jsonify({'id': user.id, 'name': user.name, 'email': user.email}), 200

# ✅ SECURED: Delete user only if no active tasks
@users_bp.route('/users/<int:id>', methods=['DELETE'])
@token_required
def delete_user(user_id, id):
    user = User.query.get_or_404(id)

    # Logical check: If user has tasks that are not completed
    pending_tasks = [t for t in user.tasks if t.status != 'completed']
    if pending_tasks:
        return jsonify({'error': 'User has pending/in-progress tasks'}), 400

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200
