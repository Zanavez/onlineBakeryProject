from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, DateField
from wtforms.validators import Length, Email, DataRequired, ValidationError, EqualTo
from datetime import datetime, timedelta


class RegTableFrom(FlaskForm):
    name = StringField("Имя", validators=[DataRequired(), Length(min=2, max=32)])
    surname = StringField("Фамилия", validators=[DataRequired(), Length(min=2, max=32)])
    patronymics = StringField("Отчество", validators=[DataRequired(), Length(min=2, max=32)])

    phone = StringField("Телефон")

    bakeries = SelectField("Пекарни", coerce=str)

    date_reg = DateField("Дата бронирования")

    submit = SubmitField("Забронировать")