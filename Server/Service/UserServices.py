from ..Repository import UserRepository
from ..database import db, User
from ..Models import PostUser, GetUser


class UserService:
    def __init__(self):
        self.__repository: UserRepository = UserRepository(db.session)

    def registration(self,
                     name: str,
                     surname: str,
                     patronymics: str,
                     phone: str,
                     email: str,
                     password: str
                     ) -> GetUser | None:
        user = PostUser(
            name=name,
            surname=surname,
            patronymics=patronymics,
            email=email,
            phone=phone,
            password=password
        )

        role_id = self.__repository.get_role_by_name("user").id
        user.id_role = role_id
        user_entity = self.__repository.add(user)
        if user_entity is not None:
            user = GetUser.model_validate(user_entity, from_attributes=True)
            return user
        return None

    def get_list_by_user(self) -> list[User]:
        return self.__repository.get_list_by_user()

    def get_user_by_uuid(self, uuid: str) -> User:
        return self.__repository.get_user_by_uuid(uuid)

    def update_user(self, uuid: str, name: str, surname: str, patronymics: str, phone: str, email: str):
        user_entity = self.__repository.get_user_by_uuid(uuid)

        user_entity.name = name
        user_entity.surname = surname
        user_entity.patronymics = patronymics
        user_entity.phone = phone
        user_entity.email = email

        self.__repository.update(user_entity)