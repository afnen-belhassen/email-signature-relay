from fastapi import FastAPI, HTTPException

from user_service import get_user_by_email

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Email Signature Relay API is running"}


@app.get("/users/{email}")
def get_user(email: str):

    user = get_user_by_email(email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user