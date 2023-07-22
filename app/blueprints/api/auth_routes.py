from . import bp as api
from flask import request, jsonify
from flask_jwt_extended import create_access_token, unset_jwt_cookies, jwt_required
from app.models import User


@api.post('/sign-up')
def sign_up():
    content, response = request.json, {}
    if User.query.filter_by(email=content['email']).first():
        response['email error'] = f'{content["email"]} email is already taken. Try again.'
    if User.query.filter_by(username=content['username']).first():
        response['username error'] = f'{content["username"]} username is already taken. Try again.'
    if 'password' not in content:
        response['password error'] = 'Please include a valid password.'
    user = User()
    user.from_dict(content)
    try:
        user.hash_password(user.password)
        user.commit()
        return jsonify({'Success': f'{user.username} is signed up.'}),200
    except:
        return jsonify(response),400


@api.post('/sign-in')
def sign_in():
    email, password = request.json.get('email'), request.json.get('password')
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.username)
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Invalid email or password. Try again.'}), 401


@api.post('/logout')
def logout():
    response = jsonify({ 'message' : 'Successfully logged out.'})
    unset_jwt_cookies(response)
    return response


@api.delete('/delete-user/<username>')
@jwt_required()
def delete_user(username):
    content = request.json
    if 'password' in content:
        password = content['password']
    else:
        return jsonify({'message' : 'Must inclued password in request'}),400
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        user.delete()
        for post in user.posts:
            post.delete()
        return jsonify({'message' : 'Username: {user.username} account deleted.'}),200
    return jsonify({'message' : 'Invalid username or password.'}),400