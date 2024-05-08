from datetime import datetime

from apps import db

class Category(db.Model):

    __tablename__ = 'category'

    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Properties
    name = db.Column(db.String(255), nullable=False)