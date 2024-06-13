from flask_login import current_user
from flask_admin.menu import MenuLink


class LogoutMenuLink(MenuLink):

    def is_accessible(self):
        return current_user.is_authenticated
