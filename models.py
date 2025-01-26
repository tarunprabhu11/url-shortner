# models.py

from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class URL(db.Model):
    __tablename__ = 'urls'  # Explicitly specify the table name

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    access_count = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<URL {self.short_code}>'
