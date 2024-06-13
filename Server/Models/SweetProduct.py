from pydantic import BaseModel


class Type(BaseModel):
    id: int
    name: str
    description: str | None


class Ingredient(BaseModel):
    id: int
    name: str
    description: str


class BaseSweetProduct(BaseModel):
    name: str
    price_sweet: float
    weight_sweet: int
    description: str
    image: str
    ingredients: list[Ingredient]


class GetSweetProduct(BaseSweetProduct):
    id: int
    trace_id: str
    type_id: int
    type: Type


class OrderToSweetProduct(BaseModel):
    id_order: int | None = None
    id_sweet_product: int | None = None
    sweet_product: GetSweetProduct
    price: float
    count: int = 0
