from sqlalchemy.orm import Session
from backend.models import Customer, User
from backend.schemas import CustomerCreate, UserCreate


def create_customer(db: Session,customer: CustomerCreate):

    db_customer = Customer(
        customer_id=customer.customer_id,
        recency=customer.recency,
        frequency=customer.frequency,
        monetary=customer.monetary,
        total_quantity=customer.total_quantity,
        unique_products=customer.unique_products,
        country=customer.country
    )

    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)

    return db_customer


def get_customers(db: Session):
    return db.query(Customer).all()


def get_customer(db: Session,customer_id: str):
    return db.query(Customer).filter(Customer.customer_id == customer_id).first()


def update_customer(db: Session,customer_id: str,customer_data: CustomerCreate):

    customer = get_customer(db,customer_id)

    if not customer:
        return None

    customer.recency = customer_data.recency
    customer.frequency = customer_data.frequency
    customer.monetary = customer_data.monetary
    customer.total_quantity = customer_data.total_quantity
    customer.unique_products = customer_data.unique_products
    customer.country = customer_data.country

    db.commit()
    db.refresh(customer)

    return customer


def delete_customer(db: Session,customer_id: str):

    customer = get_customer(db,customer_id)

    if not customer:
        return None

    db.delete(customer)
    db.commit()

    return customer


def get_user_by_username(db: Session,username: str):

    return db.query(User).filter(User.username == username).first()


def create_user( db: Session,user: UserCreate,hashed_password: str):

    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user