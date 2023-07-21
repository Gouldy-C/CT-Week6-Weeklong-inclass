from app import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(75), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    
    def commit(self):
        db.session.add(self)
        db.session.commit()
    
    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def from_dict(self, user_dict):
        for k, v in user_dict.items():
            setattr(self, k, v)
    
    def get_id(self):
        return str(self.user_id)
    
    def to_dict(self):
        return {
            'first_name' : self.first_name,
            'last_name' : self.last_name,
            'email' : self.email,
            'username' : self.username,
            'posts' : [{'body': post.body,
                        'timestamp' : post.timestamp} for post in self.posts]
        }

class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(), nullable=False)
    timestamp = db.Column(db.DateTime,
                        default=datetime.utcnow,
                        nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.user_id'),
                        nullable=False)
    
    def commit(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
