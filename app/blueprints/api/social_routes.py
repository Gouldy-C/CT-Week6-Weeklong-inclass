from . import bp as api
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models import Post, User


@api.post('/publish-post')
@jwt_required()
def publish_post():
    body = request.json.get('body')
    user = get_jwt_identity()
    user = User.query.filter_by(username=user).first()
    try:
        p = Post(body=body, user_id=user.user_id)
        p.commit()
    except:
        return jsonify({'error': 'invalid post, try again'}), 401
    return jsonify({'message': 'Posted successfully',
                    'loged in as' : user.username}), 200



@api.get('/user-posts/<username>')
@jwt_required()
def get_user_posts(username):
    user = User.query.filter_by(username=username).first()
    if user:
        user_posts = user.posts
        return jsonify({
            'message': 'Success',
            'posts' : [{'body': post.body,
                        'timestamp' : post.timestamp} for post in user_posts]
        }),200
    return jsonify({'error' : 'Not a valid username'}),401


@api.delete('/delete-post/<post_id>')
@jwt_required()
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify(message = 'Invalid Post Id'),401
    if post.author.username != get_jwt_identity():
        return jsonify(message = 'You are not allowed to delete this post'),401
    post.delete()
    return jsonify(message = 'Posted deleted'),200

@api.get('/user-profile/<username>')
@jwt_required()
def user_profile(username):
    user = User.query.filter_by(username= username).first()
    if user:
        return jsonify(user = user.to_dict()),200
    return jsonify(error = 'Invalid username')