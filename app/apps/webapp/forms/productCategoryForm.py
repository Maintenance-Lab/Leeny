from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class ProductCategoryForm(FlaskForm):
    category_name = StringField('Category name', validators=[DataRequired()])