import marshmallow as ma

class ManufacturerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'address', 'phone', 'email', 'website', 'created_at', 'updated_at')
        ordered = True

manufacturer_schema = ManufacturerSchema()
manufacturers_schema = ManufacturerSchema(many=True)