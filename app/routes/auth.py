from flask import Blueprint, request, jsonify
from app.models import db, User
from app.utils.auth import generate_token
import re

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({'error': 'Invalid email format'}), 400

    existing = User.query.filter_by(email=email).first()
    if existing:
        return jsonify({'error': 'User already exists'}), 400

    user = User(name=data['name'], email=email)
    db.session.add(user)
    db.session.commit()

    token = generate_token(user.id)
    return jsonify({'token': token}), 201

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'Invalid email'}), 401

    token = generate_token(user.id)
    return jsonify({'token': token}), 200