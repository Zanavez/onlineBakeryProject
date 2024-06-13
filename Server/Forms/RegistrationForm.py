from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Length, Email, DataRequired, ValidationError, EqualTo
from re import search


class RegistrationForm(FlaskForm):
    name = StringField("Имя", validators=[DataRequired(), Length(min=2, max=32)])
    surname = StringField("Фамилия", validators=[DataRequired(), Length(min=2, max=32)])
    patronymics = StringField("Отчество", validators=[DataRequired(), Length(min=2, max=32)])

    email = StringField("Email ", validators=[Email(message="Почта набрана неправильно")])
    phone = StringField("Телефон")

    password = PasswordField('Пароль', [
        DataRequired(),
        EqualTo('confirm', message='Пароли не совпадают')
    ])
    confirm = PasswordField('Повторите пароль')

    submit = SubmitField("Регистрация")

    def validate_phone(form, field):
        if not search(r"^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$", field.data):
            raise ValidationError("Телефон набранн не правильно")

    def validate_password(form, field):
        if not search(r"((?=.*[0-9])(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z!@#$%^&*]{6,})", field.data):
            raise ValidationError("Пароль должен содержать 1 цифру, любой уникальный символ, Буквы латинского алфавита")