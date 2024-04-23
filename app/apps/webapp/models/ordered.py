from datetime import datetime

from apps import db

class Ordered(db.Model):

    __tablename__ = 'Ordered'

    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # Foreign keys
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'))

    # Properties
    ordered = db.Column(db.Integer, nullable=False, default=0)
    delivered = db.Column(db.Integer, nullable=False, default=0)

    # Timestamps
    created_at_ts = db.Column(db.Integer, default=int(datetime.now().timestamp()))
    updated_at_ts = db.Column(db.Integer, default=int(datetime.now().timestamp()), onupdate=int(datetime.now().timestamp()))

    # Relationships
    product = db.relationship('Product', backref='ordered')
    vendor = db.relationship('Vendor', backref='ordered')