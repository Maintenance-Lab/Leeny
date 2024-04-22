import marshmallow as ma

class ProductCategorySchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'created_at', 'updated_at')
        ordered = True

product_category_schema = ProductCategorySchema()
product_categories_schema = ProductCategorySchema(many=True)