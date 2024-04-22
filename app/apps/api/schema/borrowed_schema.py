import marshmallow as ma

class BorrowedSchema(ma.Schema):
    class Meta:
        fields = ('id', 'borrower', 'borrowed_date', 'returned_date', 'created_at', 'updated_at')
        ordered = True

borrowed_schema = BorrowedSchema()
borroweds_schema = BorrowedSchema(many=True)