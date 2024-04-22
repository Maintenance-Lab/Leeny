from apps import db


class Manufacturer(db.Model):

    __tablename__ = 'manufacturer'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Properties
    name = db.Column(db.String(255), nullable=False)