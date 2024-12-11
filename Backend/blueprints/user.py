from flask import Blueprint, jsonify
from models import User
from utils.helpers import login_required

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile', methods=['GET'])
@login_required
def profile(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({
        'username': user.username,
        'email': user.email or 'Not provided',
        'registration_date': user.registration_date.strftime('%Y-%m-%d')
    })
