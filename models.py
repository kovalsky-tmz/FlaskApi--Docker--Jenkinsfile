
try:
    from __main__ import db
except:
    from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    def __repr__(self):
        return '<User %r>' % self.username

class Post(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(40),unique=False,nullable=False)
    content=db.Column(db.String(140),unique=False,nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    