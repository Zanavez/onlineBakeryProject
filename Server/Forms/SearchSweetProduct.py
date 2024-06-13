from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField


class SearchSweetProduct(FlaskForm):
    tag = SelectField("Тип продукта", coerce=int)
    submit = SubmitField("Найти")