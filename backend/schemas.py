from datetime import datetime
from pydantic import BaseModel

class CustomerCreate(BaseModel):
    customer_id: str
    recency: float
    frequency: float
    monetary: float
    total_quantity: float
    unique_products: float
    country: str | None = None
