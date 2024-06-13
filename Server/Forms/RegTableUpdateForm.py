from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, DateField
from wtforms.validators import Length, Email, DataRequired, ValidationError, EqualTo
from datetime import datetime, timedelta


class RegTableUpdateFrom(FlaskForm):
    state_reg = SelectField("Статус регистрации", choices=[
        ("waiting_for_payment", "Ждет подтверждения"),
        ("confirmed", "Подверждено")
    ])
    table = SelectField("Пекарни", coerce=int)
    start_time = SelectField("Пекарни", coerce=int)
    end_time = SelectField("Пекарни", coerce=int)
    date_reg = DateField("Дата бронирования")

    submit = SubmitField("Сохранить")