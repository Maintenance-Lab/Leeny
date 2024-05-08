from datetime import datetime

from apps import db

class Order(db.Model):

    __tablename__ = 'order'

    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # Foreign keys
    ordered_id = db.Column(db.Integer, db.ForeignKey('ordered.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))

    # Timestamps
    created_at_ts = db.Column(db.Integer, default=int(datetime.now().timestamp()))
    updated_at_ts = db.Column(db.Integer, default=int(datetime.now().timestamp()), onupdate=int(datetime.now().timestamp()))

