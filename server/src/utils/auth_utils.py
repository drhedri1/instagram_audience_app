# Placeholder for authentication related functions (e.g., JWT generation, verification)
# We might use Flask-Login or Flask-JWT-Extended later if needed

import jwt
import datetime
from flask import current_app, request, jsonify
from functools import wraps
from src.models.user import User

def generate_token(user_id):
    """Generates the Auth Token"""
    try:
        payload = {
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1, seconds=0),
            'iat': datetime.datetime.now(datetime.timezone.utc),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            current_app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e

def decode_token(token):
    """Decodes the auth token"""
    try:
        payload = jwt.decode(token, current_app.config.get('SECRET_KEY'), algorithms=['HS256'])
        return payload['sub'] # Return user_id
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'

# Decorator for protected routes
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Check for token in Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'message': 'Bearer token malformed!'}), 401

        if not token:
            # Check for token in cookies as fallback (adjust cookie name if needed)
            token = request.cookies.get('auth_token')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            user_id = decode_token(token)
            if isinstance(user_id, str): # Error message returned from decode_token
                return jsonify({'message': user_id}), 401

            current_user = User.query.get(user_id)
            if not current_user:
                 return jsonify({'message': 'User not found!'}), 401

        except Exception as e:
            current_app.logger.error(f"Token validation error: {e}")
            return jsonify({'message': 'Token is invalid!'}), 401

        # Pass user object or user_id to the decorated function
        return f(current_user, *args, **kwargs)

    return decorated

