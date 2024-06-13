from flask_admin.contrib.sqla import ModelView
from ..database import User
from wtforms import PasswordField
from uuid import uuid4


class UserAdminView(ModelView):
    excluded_list_columns = ("password_hash", )
    form_extra_fields = {
        'password_hash': PasswordField('Password')
    }
    form_columns = [
        'name',
        'surname',
        'patronymics',
        'phone',
        'email',
        'data_bith',
        'passport_series',
        'passport_number',
        "password_hash",
        "role"
    ]

    def on_model_change(self, form, model: User, is_created):
        model.password = form.password_hash.data
        model.trace_id = str(uuid4())