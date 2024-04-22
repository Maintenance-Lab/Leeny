import marshmallow as ma

class VendorSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'address', 'phone', 'email', 'website', 'created_at', 'updated_at')
        ordered = True

vendor_schema = VendorSchema()
vendors_schema = VendorSchema(many=True)