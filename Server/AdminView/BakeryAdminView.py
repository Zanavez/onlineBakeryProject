from uuid import uuid4
from flask_admin.contrib.sqla import ModelView
from Server.database import Bakery


class BakeryAdminView(ModelView):

    form_columns = [
        'name',
        'address',
        'description'
    ]

    def on_model_change(self, form, model: Bakery, is_created):
        model.trace_id = str(uuid4())