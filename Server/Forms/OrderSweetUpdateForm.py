from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, IntegerField
from wtforms.validators import Length, Email, DataRequired, ValidationError, EqualTo


class OrderSweetUpdateForm(FlaskForm):
    count = IntegerField("Количество: ", validators=[DataRequired()])
    submit = SubmitField("Сохранить")