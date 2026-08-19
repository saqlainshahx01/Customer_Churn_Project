from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import engine, Base ,get_db
from backend.models import Customer ,User
from backend.schemas import (
    CustomerCreate,
    CustomerResponse,
    UserCreate,
    UserResponse,
    LoginRequest,
    PredictionRequest,
    PredictionResponse
)
from backend.ml_prediction import predict_customer

from backend.crud import (
    create_customer,
    get_customers,
    get_customer,
    update_customer,
    delete_customer,
    get_user_by_username,
    create_user
)
from backend.utils import (
    hash_password,
    verify_password
)

from backend.auth import create_token ,verify_token 

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Customer Churn API",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "Customer Churn API is running"
    }

@app.post(
    "/customers",
    response_model=CustomerResponse
)
def add_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):

    return create_customer(db,customer)

@app.get(
    "/customers",
    response_model=list[CustomerResponse]
)
def read_customers(
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):

    return get_customers(db)


@app.get(
    "/customers/{customer_id}",
    response_model=CustomerResponse
)
def read_customer(
    customer_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)  
):

    customer = get_customer(
        db,
        customer_id
    )

    if not customer:

        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer

@app.put(
    "/customers/{customer_id}",
    response_model=CustomerResponse
)
def edit_customer(
    customer_id: str,
    customer_data: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):

    customer = update_customer(
        db,
        customer_id,
        customer_data
    )

    if not customer:

        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer


@app.delete(
    "/customers/{customer_id}"
)
def remove_customer(
    customer_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)  
):

    customer = delete_customer(
        db,
        customer_id
    )

    if not customer:

        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return {
        "message": "Customer deleted successfully"
    }

@app.post("/predict",response_model=PredictionResponse)
def predict_new_customer(data: PredictionRequest,current_user: dict = Depends(verify_token)):

    result = predict_customer(
        recency=data.recency,
        frequency=data.frequency,
        monetary=data.monetary,
        total_quantity=data.total_quantity,
        unique_products=data.unique_products
    )

    return result 

@app.get("/customers/{customer_id}/predict",response_model=PredictionResponse)
def predict_existing_customer(customer_id: str,db: Session = Depends(get_db),current_user: dict = Depends(verify_token)):

    customer = get_customer(db,customer_id)

    if not customer:

        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    result = predict_customer(
        recency=customer.recency,
        frequency=customer.frequency,
        monetary=customer.monetary,
        total_quantity=customer.total_quantity,
        unique_products=customer.unique_products
    )

    return result   

@app.post(
    "/auth/signup",
    response_model=UserResponse
)
def signup(
    user: UserCreate,
    db: Session = Depends(get_db),

):

    existing_user = get_user_by_username(
        db,
        user.username
    )

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    hashed_password = hash_password(
        user.password
    )

    return create_user(
        db,
        user,
        hashed_password
    )


@app.post("/auth/login")
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):

    user = get_user_by_username(
        db,
        login_data.username
    )

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    password_correct = verify_password(
        login_data.password,
        user.hashed_password
    )

    if not password_correct:

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    token = create_token({
        "sub": str(user.id),
        "username": user.username
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }    

