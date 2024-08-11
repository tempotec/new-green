from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash


db = SQLAlchemy()

class Evaluation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    evaluator_name = db.Column(db.String(100), default='Convidado')  # Nome aleatório padrão
    company = db.Column(db.String(100), nullable=False)
    cleanliness = db.Column(db.Integer)
    organization = db.Column(db.Integer)
    presentation = db.Column(db.Integer, default=0)
    food_quality = db.Column(db.Integer, default=0)
    comments = db.Column(db.String(500))



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)  # Adicione esta linha

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
