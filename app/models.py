from datetime import datetime
from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    comment = db.relationship('Comment', backref='author', lazy='dynamic')
    homework = db.relationship('Homework', backref='student', lazy='dynamic')
    about_me = db.Column(db.String(140))
    status = db.Column(db.String(30))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Comment {}>'.format(self.body)

class Homework(db.Model):
    __tablename__ = 'homework'
    id = db.Column(db.Integer, primary_key=True)
    comment_before = db.Column(db.String(200))
    comment_after = db.Column(db.String(200))
    finished = db.Column(db.Boolean)
    result = db.Column(db.Float(5))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    # task = db.relationship('task', backref='current_hw', lazy='dynamic')

    def __repr__(self):
        return '<Homework {}>'.format(self.id)

class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer)
    theme = db.Column(db.String(40))
    name = db.Column(db.String(40))
    course = db.Column(db.String(40))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    homework = db.relationship('Homework', backref='current_task', lazy='dynamic')
    body = db.Column(db.Text)
    # homework_id = db.Column(db.Integer, db.ForeignKey('homework.id'))
    # subtask = db.relationship('Subtask', backref='task', lazy='dynamic')

    def __repr__(self):
        return '<Task {}>'.format(self.name)

# class Subtask(db.Model):
#     __tablename__ = 'subtask'
#     id = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.String(1200))
#     task_id = db.Column(db.Integer, db.ForeignKey('task.id'))

#     def __repr__(self):
#         return '<Subtask {}>'.format(self.id)

class Answers(db.Model):
    __tablename__ = 'answerks'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(300))
    comments = db.Column(db.String(300))
    homework_id = db.Column(db.Integer, db.ForeignKey('homework.id'))

    def __repr__(self):
        return '<Answers {}>'.format(self.body)

