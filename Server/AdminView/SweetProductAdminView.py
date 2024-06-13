from flask_admin.contrib.sqla import ModelView
from flask_admin.form import ImageUploadField
from random import getrandbits

from markupsafe import Markup

from Server.database import SweetProduct
from uuid import uuid4
import os
from flask import url_for


file_path = os.path.abspath(os.path.dirname(__name__))


def name_gen_image(model, file_data) -> str:
    return str(getrandbits(20))


def list_thumbnail(view, content, model: SweetProduct, name):
    url = url_for('static', filename=os.path.join('img/', model.image))
    return Markup(f"<img src={url} width=100>")


class SweetProductAdminView(ModelView):
    form_columns = [
        'name',
        'price_sweet',
        'weight_sweet',
        'description',
        'ingredients',
        'type',
        'image'
    ]
    form_extra_fields = {
        'image': ImageUploadField('file',
                                  base_path=os.path.join(file_path, "static/img/"),
                                  url_relative_path='img/',
                                  namegen=name_gen_image,
                                  allowed_extensions=['jpg', 'png', 'jpeg'],
                                  max_size=(1200, 780, True),
                                  thumbnail_size=(100, 100, True))
    }

    column_formatters = {
        "image": list_thumbnail
    }

    def create_form(self, obj=None):
        return super(SweetProductAdminView, self).create_form(obj)

    def edit_form(self, obj=None):
        return super(SweetProductAdminView, self).edit_form(obj)

    def on_model_change(self, form, model: SweetProduct, is_created):
        model.trace_id = str(uuid4())
