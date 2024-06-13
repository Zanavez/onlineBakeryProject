from .User import GetUser
from flask import session


class UserSession:
    def __init__(self, user: GetUser | None):
        self.__user: GetUser | None = user

    def get_count_car(self) -> int:
        return len(session["car"])

    @property
    def user(self):
        return self.__user

    def is_authenticated(self):
        if self.__user is not None:
            return True
        return False

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.__user.id)