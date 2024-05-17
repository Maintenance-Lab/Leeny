from apps import db

class Vendor(db.Model):

    __tablename__ = 'vendor'

    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # Properties
    vendor_name = db.Column(db.String(255), nullable=False)
    website = db.Column(db.String(255))
