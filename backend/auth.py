from datetime import datetime, timedelta, timezone
from fastapi import Header, HTTPException
from jose import jwt, JWTError

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=2)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)


def verify_token(authorization: str = Header(...)):

    if not authorization.startswith("Bearer "):

        raise HTTPException(status_code=401,detail="Invalid authorization header")

    token = authorization.replace("Bearer ","",1)

    try:

        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])

        return payload

    except JWTError:

        raise HTTPException(status_code=401,detail="Invalid or expired token")