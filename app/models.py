from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, index=True)
    profile = db.Column(db.String)
    prof_pic = db.Column(db.String())
    blog_post = db.relationship("Blog", backref="user", lazy="dynamic")
    pass_hash = db.column(db.String(255))

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    @property
    def password(self):
        raise AttributeError('Stick to your lane!')

    @password.setter
    def password(self, password):
        self.pass_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_hash, password)

    def get_blogs(self):
        user = User.query.filter_by(id=self.id).first()
        return user.blog

    def __repr__(self):
        return f'User {self.username}'

class Blog(db.Model):
    '''
    Pitch class to define pitch objects
    '''
    __tablename__ = "blogs"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    title = db.Column(db.String)
    category = db.Column(db.String)
    pitch = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def save_blog(self):
        db.session.add(self)
        db.session.commit()
