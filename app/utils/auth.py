import jwt
from datetime import datetime, timedelta
from flask import request, jsonify
from functools import wraps

SECRET_KEY = "your-secret-key"  # 🔒 replace with a secure key in .env

def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(minutes=30)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]  # Bearer <token>

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        user_id = decode_token(token)
        if not user_id:
            return jsonify({'message': 'Invalid or expired token'}), 401

        return f(user_id=user_id, *args, **kwargs)

    return decorated
