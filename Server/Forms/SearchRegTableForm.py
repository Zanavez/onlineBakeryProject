from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField


class SearchRegTableForm(FlaskForm):
    state_order = SelectField("Статус регистрации", choices=[
        ("waiting_for_confirmation", "Ждет подтверждения"),
        ("confirmed", "Подверждено")
    ])
    submit = SubmitField("Найти")