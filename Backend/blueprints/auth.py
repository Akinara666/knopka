from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from utils.helpers import create_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    login_name = data.get('login')
    password = data.get('password')

    if User.query.filter((User.login == login_name)|(User.username == username)).first():
        return jsonify({'error': 'Username or login already exists'}), 400

    password_hash = generate_password_hash(password)
    user = User(username=username, login=login_name, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    login_name = data.get('login')
    password = data.get('password')

    user = User.query.filter_by(login=login_name).first()
    if user and check_password_hash(user.password_hash, password):
        token = create_token(user.id)
        return jsonify({'token': token, 'username': user.username}), 200

    return jsonify({'error': 'Invalid credentials'}), 401
