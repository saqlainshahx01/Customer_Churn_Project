from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func

from database import Base


class Customer(Base):

    __tablename__ = "customers"

    # =========================
    # Primary Key
    # =========================

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Customer Information

    customer_id = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    country = Column(
        String(100),
        nullable=True
    )


    # ML Features

    recency = Column(
        Float,
        nullable=False
    )

    frequency = Column(
        Float,
        nullable=False
    )

    monetary = Column(
        Float,
        nullable=False
    )

    total_quantity = Column(
        Float,
        nullable=False
    )

    unique_products = Column(
        Float,
        nullable=False
    )

    # Timestamps

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )