from api.models import User, db
from flask import request, jsonify, g, Blueprint
from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
auth = HTTPTokenAuth(scheme='Bearer')

auth_view = Blueprint('auth_view', __name__, url_prefix='/auth')


@auth.verify_token
def verify_auth_token(token):
    if not token:
        return jsonify({"message": "supply token"}), 401
    user_id = User.verify_auth_token(token=token)
    if not token:
        return False
    g.user = db.session.query(User).filter_by(id=user_id).first()
    return True


def verify_password(username, password):
    user = db.session.query(User).filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    return user


@auth_view.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({'message': 'Please enter username and password'}), 400

    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({'message': 'User already exists!'}), 400

    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registration successful!'}), 201


@auth_view.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    if not username or not password:
        return jsonify({'message': 'Please enter password and Username'}), 400
    user = verify_password(username, password)
    if user:
        g.user = user
        token = g.user.generate_token().decode("ascii")
        return jsonify({
            "token": "Bearer {}".format(token)
        })
    else:
        return jsonify({'message': 'invalid username/password'}), 400
