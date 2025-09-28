from dataclasses import dataclass

@dataclass
class Product:
    name: str
    type: str
    category: str
    subcategory: str
    brand: str
    sellers: list[str]
    product_id: int
    price: float
    updated_at: str
    url: str