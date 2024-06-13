from ..Repository import SweetProductRepository, BakeryRepository, OrderRepository
from ..database import db, Bakery, TypeOrder, Order, Type
from ..Models import GetSweetProduct, OrderToSweetProduct, BaseOrder, GetOrder, OrderView


class ShopService:
    def __init__(self):
        self.__sweet_repository: SweetProductRepository = SweetProductRepository(db.session)
        self.__bakery_repository: BakeryRepository = BakeryRepository(db.session)
        self.__order_repository: OrderRepository = OrderRepository(db.session)
        self.__count_sweet: int = 20
        self.__count_row: int = self.__sweet_repository.count_row()

    def get_sweet_product_page(self, page: int):
        pass

    def get_list_bakery(self) -> list[Bakery]:
        return self.__bakery_repository.get_list()

    def get_address_by_bakery_uuid(self, uuid: str) -> str:
        return self.__bakery_repository.get_by_uuid(uuid).address

    def get_bakery_uuid(self, uuid: str) -> Bakery:
        return self.__bakery_repository.get_by_uuid(uuid)

    def get_list_tag(self) -> list[Type]:
        return self.__sweet_repository.get_list_tag()

    def get_sweet_product_by_tag(self, tag: int):
        sweet_products_entity = self.__sweet_repository.get_sweet_product_by_tag(tag)
        sweet_products = [GetSweetProduct.model_validate(i, from_attributes=True) for i in sweet_products_entity]
        for i in sweet_products:
            name, ext = i.image.split(".")
            i.image = f"{name}_thumb.{ext}"
        return sweet_products

    def get_sweet_product(self) -> list[GetSweetProduct]:
        sweet_products_entity = self.__sweet_repository.get_sweet_product()
        sweet_products = [GetSweetProduct.model_validate(i, from_attributes=True) for i in sweet_products_entity]
        for i in sweet_products:
            print(i.image)
            name, ext = i.image.split(".")
            i.image = f"{name}_thumb.{ext}"
        return sweet_products

    def get_product(self, uuid: str) -> GetSweetProduct | None:
        sweet_product_entity = self.__sweet_repository.get_by_uuid(uuid)
        try:
            sweet_product = GetSweetProduct.model_validate(sweet_product_entity, from_attributes=True)
        except:
            sweet_product = None

        return sweet_product

    def get_list_product_by_uuid(self, uuids: list[str], counts: dict) -> list[OrderToSweetProduct]:
        list_sweet_product = []
        for uuid in uuids:
            list_sweet_product.append(self.__sweet_repository.get_by_uuid(uuid))
        return [OrderToSweetProduct(
            id_sweet_product=sweet_product.id,
            sweet_product=GetSweetProduct.model_validate(sweet_product, from_attributes=True),
            price=sweet_product.price_sweet,
            count=counts[sweet_product.trace_id]
        ) for sweet_product in list_sweet_product]

    def create_order(self, type_order: TypeOrder, address: str, description: str, cart: dict, user_id: int) -> Order:
        list_order_to_sweet_product = self.get_list_product_by_uuid(list(cart.keys()), cart)
        order = BaseOrder(
            user_id=user_id,
            type_order=type_order,
            address=address,
            description=description,
            sweet_products=list_order_to_sweet_product
        )
        order = self.__order_repository.add(order)
        return order

    def get_list_order_by_user_id(self, id_user: int) -> list[OrderView]:
        list_order_entity = self.__order_repository.get_list_order_by_user_id(id_user)
        orders = [OrderView.model_validate(i, from_attributes=True) for i in list_order_entity]

        for order in orders:
            sum_price = sum([i.price * i.count for i in order.sweet_products])
            order.sum_price = sum_price

        return orders

    def get_order_by_uuid(self, uuid: str) -> Order:
        return self.__order_repository.get_by_uuid(uuid)
