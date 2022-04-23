from plan import bcrypt, login_manager
from plan import db
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    tasks_user = db.relationship("Todo")

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_pasword):
        self.password_hash = bcrypt.generate_password_hash(plain_text_pasword).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

class Todo(db.Model): 
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False)
    description = db.Column(db.String(length=1024), nullable=False)
    done = db.Column(db.Boolean, default=False)
    owner = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return f'{self.name}'





