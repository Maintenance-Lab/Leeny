import marshmallow as ma

class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'created_at', 'updated_at')
        ordered = True

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)