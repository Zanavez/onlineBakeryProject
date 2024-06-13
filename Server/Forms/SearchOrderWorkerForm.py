from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField


class SearchOrderWorkerForm(FlaskForm):
    state_order = SelectField("Статус заказа", choices=[
        ("confirmed", "Подтверждено"),
        ("prepared", "Готовиться"),
        ("ready", "Готово")
    ])
    type_order = SelectField("Тип заказа", choices=[
        ("in_hall", "В зале"),
        ("with_myself", "Доставка")
    ])
    submit = SubmitField("Найти")