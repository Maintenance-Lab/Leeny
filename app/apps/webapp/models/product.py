from datetime import datetime

from apps import db


class Product(db.Model):

    __tablename__ = 'product'

    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # Properties
    title = db.Column(db.String(255), nullable=False)
    barcode = db.Column(db.String(255), nullable=True)
    # price_when_bought = db.Column(db.Float, nullable=False)
    priceBTW = db.Column(db.Float)
    priceNoBTW = db.Column(db.Float)
    description = db.Column(db.Text)
    url = db.Column(db.String(255))
    documentation = db.Column(db.String(255))
    notes = db.Column(db.String(10000))
    quantity_unavailable = db.Column(db.Integer, default=0)
    quantity_total = db.Column(db.Integer)
    quantity_borrowed = db.Column(db.Integer, default=0)

    # Timestamps
    created_at_ts = db.Column(db.Integer, default=int(datetime.now().timestamp()))
    # updated_at_ts = db.Column(db.Integer, default=int(datetime.now().timestamp()), onupdate=int(datetime.now().timestamp()))

    # Foreign keys
    manufacturer_id = db.Column(db.Integer, db.ForeignKey('manufacturer.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('productCategory.id'), nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'), nullable=False)

    # Relationships
    manufacturer = db.relationship('Manufacturer', backref='product')
    category = db.relationship('ProductCategory', backref='product')
    vendor = db.relationship('Vendor', backref='product')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'barcode': self.barcode,
            # 'price_when_bought': self.price_when_bought,
            'priceBTW': self.priceBTW,
            'priceNoBTW': self.priceNoBTW,
            'description': self.description,
            'url': self.url,
            'documentation': self.documentation,
            'notes': self.notes,
            'manufacturer_id': self.manufacturer_id,
            'category_id': self.category_id,
            'vendor_id': self.vendor_id
        }
