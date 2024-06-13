from pydantic import BaseModel, Extra
from ..database import TypeOrder, StatusOrder
from .SweetProduct import OrderToSweetProduct
from datetime import datetime


class BaseOrder(BaseModel):
    user_id: int
    type_order: TypeOrder = TypeOrder.in_hall
    status_order: StatusOrder = StatusOrder.waiting_for_confirmation
    address: str
    description: str = ""
    sweet_products: list[OrderToSweetProduct]


class GetOrder(BaseOrder):
    id: int
    trace_id: str
    datatime_order: datetime
    sum_price: float = 0


class OrderView(BaseModel, extra=Extra.forbid):
    id: int
    trace_id: str
    datatime_order: datetime
    sum_price: float = 0
    user_id: int
    type_order: TypeOrder = TypeOrder.in_hall
    status_order: StatusOrder = StatusOrder.waiting_for_confirmation
    address: str
    description: str = ""
    sweet_products: object


class OrderViewAdmin(OrderView):
    user: object


state_order = {
    1: "Ждет оплаты",
    2: "оплачено",
    3: "Ждет подтверждения",
    4: "Подтверждено",
    5: "Готовиться",
    6: "Готово",
    7: "Ждет курьера",
    8: "Доставльяеться",
    9: "Завершен"
               }

type_order = {
    1: "В зале",
    2: "Бронирование"
}
