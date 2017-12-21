from app import db


class Usuario(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50))
    passwd = db.Column(db.String(50))