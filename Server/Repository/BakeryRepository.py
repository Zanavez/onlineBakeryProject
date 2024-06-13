from sqlalchemy.orm import Session
from ..database import Bakery

from uuid import uuid4


class BakeryRepository:
    def __init__(self, session: Session):
        self.__session: Session = session

    def get_list(self) -> list[Bakery] | None:
        return self.__session.query(Bakery).all()

    def get_by_uuid(self, uuid: str) -> Bakery | None:
        return self.__session.query(Bakery).filter(Bakery.trace_id == uuid).first()

    def get_by_address(self, address: str) -> Bakery | None:
        return self.__session.query(Bakery).where(Bakery.address == address).first()