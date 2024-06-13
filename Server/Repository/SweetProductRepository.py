from sqlalchemy.orm import Session
from sqlalchemy import func, select
from ..database import SweetProduct, Type


class SweetProductRepository:
    def __init__(self, session: Session):
        self.__session: Session = session

    def count_row(self) -> int:
        response = select(func.count(SweetProduct.id))
        result = self.__session.execute(response)
        return result.scalars().first()

    def get_page_sweet_product(self, start: int, limit: int) -> list[SweetProduct]:
        sweet_product = self.__session.query(SweetProduct).offset(start).fetch(limit).order_by(SweetProduct.id).all()
        return sweet_product

    def get_sweet_product(self) -> list[SweetProduct]:
        sweet_product = self.__session.query(SweetProduct).order_by(SweetProduct.id).all()
        return sweet_product

    def get_by_uuid(self, uuid: str) -> SweetProduct | None:
        sweet_product = self.__session.query(SweetProduct).filter(SweetProduct.trace_id == uuid).first()
        return sweet_product

    def get_list_tag(self) -> Type | None:
        return self.__session.query(Type).all()

    def get_sweet_product_by_tag(self, tag: int) -> list[SweetProduct]:
        sweet_product = self.__session.query(SweetProduct).where(SweetProduct.type_id == tag).order_by(SweetProduct.id).all()
        return sweet_product