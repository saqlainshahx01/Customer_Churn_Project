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


class CustomerResponse(BaseModel):
    id: int
    customer_id: str
    recency: float
    frequency: float
    monetary: float
    total_quantity: float
    unique_products: float
    country: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True   

class UserCreate(BaseModel):

    username: str
    email: str
    password: str


class UserResponse(BaseModel):

    id: int
    username: str
    email: str

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):

    username: str
    password: str