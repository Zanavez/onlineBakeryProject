from ..Repository import OrderRepository, BakeryRepository
from ..database import db, Order, OrderToSweetProduct, Bakery, StatusOrder
from ..Models import OrderViewAdmin


class OrderService:
    def __init__(self):
        self.__repository: OrderRepository = OrderRepository(db.session)
        self.__repository_bakery: BakeryRepository = BakeryRepository(db.session)

    def get_list_order(self) -> list[OrderViewAdmin]:
        list_order_entity = self.__repository.get_list_order()
        orders = [OrderViewAdmin.model_validate(i, from_attributes=True) for i in list_order_entity]

        for order in orders:
            sum_price = sum([i.price * i.count for i in order.sweet_products])
            order.sum_price = sum_price
        return orders

    def get_list_order_by_state_order(self, state_order: str) -> list[OrderViewAdmin]:
        print(state_order)
        list_order_entity = self.__repository.get_list_order_by_state_order(state_order)
        orders = [OrderViewAdmin.model_validate(i, from_attributes=True) for i in list_order_entity]

        for order in orders:
            sum_price = sum([i.price * i.count for i in order.sweet_products])
            order.sum_price = sum_price
        return orders

    def get_order(self, uuid: str) -> OrderViewAdmin:
        order_entity = self.__repository.get_by_uuid(uuid)
        order = OrderViewAdmin.model_validate(order_entity, from_attributes=True)

        sum_price = sum([i.price * i.count for i in order.sweet_products])
        order.sum_price = sum_price
        return order

    def get_order_by_id(self, id_order: int) -> Order:
        return self.__repository.get(id_order)

    def get_order_sweet_product(self, id_order: int, id_sweet_product: int) -> OrderToSweetProduct:
        return self.__repository.get_by_id_order_and_sweet_product(id_order, id_sweet_product)

    def get_bakery_by_address(self, address: str) -> Bakery | None:
        return self.__repository_bakery.get_by_address(address)

    def delete_order_sweet_product(self, id_order: int, id_sweet_product: int):
        self.__repository.delete_by_id_order_and_sweet_product(id_order, id_sweet_product)

    def update_order_sweet_product(self, id_order: int, id_sweet_product: int, count: int):
        self.__repository.update_sweet_product(id_order, id_sweet_product, count)

    def update(self, uuid: str, address: str, state_order: object):
        order = self.__repository.get_by_uuid(uuid)
        order.address = address
        order.status_order = state_order

        self.__repository.update(order)

    def order_update_status(self, uuid: str) -> Order:
        order = self.__repository.get_by_uuid(uuid)
        if order.status_order == StatusOrder.confirmed:
            order.status_order = StatusOrder.prepared
        elif order.status_order == StatusOrder.prepared:
            order.status_order = StatusOrder.ready

        self.__repository.update(order)
        return order

