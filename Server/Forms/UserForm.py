from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Length, Email, DataRequired, ValidationError, EqualTo
from re import search


class UserForm(FlaskForm):
    name = StringField("Имя", validators=[DataRequired(), Length(min=2, max=32)])
    surname = StringField("Фамилия", validators=[DataRequired(), Length(min=2, max=32)])
    patronymics = StringField("Отчество", validators=[DataRequired(), Length(min=2, max=32)])

    email = StringField("Email ", validators=[Email(message="Почта набрана не правильно")])
    phone = StringField("Телефон")
    submit = SubmitField("Сохранить")

    def validate_phone(form, field):
        if not search(r"^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$", field.data):
            raise ValidationError("Телефон набран неправильно")