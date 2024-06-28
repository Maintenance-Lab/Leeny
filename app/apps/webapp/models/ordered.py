from datetime import datetime

from apps import db

class Ordered(db.Model):

    __tablename__ = 'ordered'

    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # Foreign keys
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    manufacturer_id = db.Column(db.Integer, db.ForeignKey('manufacturer.id'))
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('productCategory.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))

    # Properties
    title = db.Column(db.String(255), nullable=False)
    reason = db.Column(db.String(255))
    quantity = db.Column(db.Integer, nullable=False, default=1)
    url = db.Column(db.String(255))
    price_when_bought = db.Column(db.Float)
    status = db.Column(db.Integer, default=1)

    # Timestamps
    created_at_ts = db.Column(db.Integer, default=int(datetime.now().timestamp()))
    updated_at_ts = db.Column(db.Integer, default=int(datetime.now().timestamp()), onupdate=int(datetime.now().timestamp()))

    # Relationships
    product = db.relationship('Product', backref='ordered')
    vendor = db.relationship('Vendor', backref='ordered')