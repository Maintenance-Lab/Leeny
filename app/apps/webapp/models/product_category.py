from apps import db


class ProductCategory(db.Model):

    __tablename__ = 'productCategory'

    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # Properties
    category_name = db.Column(db.String(255), nullable=False)
