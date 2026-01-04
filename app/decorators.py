from functools import wraps
from flask import session, redirect, url_for, flash, jsonify, request


def role_required(roles):
    """
    Decorator to restrict access to users with specified role(s).
    Accepts a single role string or a list of role strings.
    """
    if isinstance(roles, str):
        allowed_roles = [roles]
    else:
        allowed_roles = roles
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Ensure user is logged in
            if not session.get('logged_in'):
                flash('Please log in to access this page.', 'error')
                return redirect(url_for('main.login'))
            user_role = session.get('role')
            if user_role not in allowed_roles:
                # For API endpoints, return JSON error
                if request.path.startswith('/api/') or request.is_json:
                    return jsonify({'error': 'Unauthorized access'}), 403
                flash('Unauthorized access', 'error')
                return redirect(url_for('main.home'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator 