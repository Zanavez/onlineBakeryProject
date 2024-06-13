from flask_admin import Admin, AdminIndexView
from flask_login import current_user


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.user.role.name == "admin"
        return False