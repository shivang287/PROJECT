"""Database models for the Todo app."""
from app import db

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    status = db.Column(db.String(20), default = "Pending")
