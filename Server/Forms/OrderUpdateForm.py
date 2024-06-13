from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import Length, Email, DataRequired, ValidationError, EqualTo


class OrderUpdateForm(FlaskForm):
    bakeries = SelectField("Пекарни", coerce=str)
    state_order = SelectField("Состояние заказа", coerce=str)
    address = StringField("Адресс", validators=[DataRequired()])
    submit = SubmitField("Сохранить")