from fastapi import FastAPI

from backend.database import engine, Base
from backend.models import Customer


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