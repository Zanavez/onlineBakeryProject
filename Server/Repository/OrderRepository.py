from sqlalchemy.orm import Session
from sqlalchemy import func, select
from ..database import Order, OrderToSweetProduct, StatusOrder
from ..Models import BaseOrder


class OrderRepository:
    def __init__(self, session: Session):
        self.__session: Session = session

    def add(self, order: BaseOrder) -> Order | None:
        try:
            order_entity = Order(
                user_id=order.user_id,
                type_order=order.type_order,
                status_order=order.status_order,
                address=order.address,
                description=order.description
            )

            self.__session.add(order_entity)
            self.__session.commit()

            order_to_sweet_product_list = []

            for i in order.sweet_products:
                order_to_sweet_product_list.append(OrderToSweetProduct(
                    id_order=order_entity.id,
                    id_sweet_product=i.id_sweet_product,
                    price=i.price,
                    count=i.count
                ))
            self.__session.add_all(order_to_sweet_product_list)
            self.__session.commit()
            return order_entity
        except:
            self.__session.rollback()
            return None

    def get_list_order_by_user_id(self, id_user: int) -> list[Order] | None:
        return self.__session.query(Order).filter(Order.user_id == id_user).order_by(Order.datatime_order).all()

    def get_list_order(self) -> list[Order] | None:
        return self.__session.query(Order).order_by(Order.datatime_order).all()

    def get_list_order_by_state_order(self, state_order: str) -> list[Order] | None:

        return self.__session.query(Order).where(Order.status_order == state_order).order_by(Order.datatime_order).all()

    def get_by_uuid(self, uuid: str) -> Order | None:
        return self.__session.query(Order).filter(Order.trace_id == uuid).first()

    def delete_by_id_order_and_sweet_product(self, id_order: int, id_sweet_product: int):
        order_entity = self.__session.query(OrderToSweetProduct).where(OrderToSweetProduct.id_order == id_order)\
            .where(OrderToSweetProduct.id_sweet_product == id_sweet_product).first()
        try:
            self.__session.delete(order_entity)
            self.__session.commit()
        except:
            self.__session.rollback()

    def get(self, id: int) -> Order | None:
        return self.__session.get(Order, id)

    def get_by_id_order_and_sweet_product(self, id_order: int, id_sweet_product: int) -> OrderToSweetProduct | None:
        return self.__session.query(OrderToSweetProduct).\
            where(OrderToSweetProduct.id_order == id_order).\
            where(OrderToSweetProduct.id_sweet_product == id_sweet_product).first()

    def update_sweet_product(self, id_order: int, id_sweet_product: int, count: int):
        order_sweet_product = self.get_by_id_order_and_sweet_product(id_order, id_sweet_product)
        order_sweet_product.count = count
        self.__session.commit()

    def update(self, order: Order):
        try:
            self.__session.add(order)
            self.__session.commit()
        except:
            self.__session.rollback()