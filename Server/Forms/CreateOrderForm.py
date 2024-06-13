from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, SelectField, HiddenField, DateField
from wtforms.validators import DataRequired, Length


class CreateOrderForm(FlaskForm):
    bakeries = SelectField("Пекарни", coerce=str)
    city = StringField("Город", validators=[])
    street = StringField("Улица", validators=[])
    home = IntegerField("Дом", validators=[])
    apartment = IntegerField("Квартира", validators=[])
    floor = IntegerField("Этаж", validators=[])
    date_reg = DateField("Дата бронирования")
    type_order = HiddenField()
    description = TextAreaField("Комментарии к заказу")
    type_payment = SelectField("Тип оплаты", choices=[("1", "Оплата при получении")])
    submit = SubmitField("Заказать")