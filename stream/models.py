from datetime import datetime
from stream import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return accounts.query.get(int(user_id))


class accounts(db.Model, UserMixin):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    passwd = db.Column(db.String(120), nullable=False)
    usage = db.relationship('logs',  backref='user_log', lazy=True)

    def __repr__(self):
        return f"User('{self.user}', '{self.email}')"


class logs(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, default='Rasp001')
    in_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey(accounts.id), nullable=False)

    def __repr__(self):
        return f"Device('{self.name}')"


class weather(db.Model):
    __tablename__ = 'weather'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    temp = db.Column(db.Integer, nullable=False)
    light = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Weather('{self.timestamp}', '{self.temp}', '{self.light}')"
# Table schema for many to many


'''
conn = db.Table('conn', db.Column('user_id', db.Integer, db.ForeignKey('account.id')), db.Column('node-id', db.Integer, db.ForeignKey('node.id')))


class account(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    passwd = db.Column(db.String(20), nullable=False)
    node_auth = db.relationship('node', secondary=conn, backref=db.backref('user_auth', lazy='dynamic'))

    def __repr__(self):
        return f"User('{self.user}', '{self.email}')"


class node(db.Model):
    __tablename__ = 'node'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return f"Device('{self.name}')"
'''
