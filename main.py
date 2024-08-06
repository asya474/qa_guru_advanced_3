from typing import List, Union
from fastapi import FastAPI, HTTPException
from fastapi_pagination import Page, add_pagination, paginate
from models.AppStatus import AppStatus
from models.User import User
import json
from http import HTTPStatus
import uvicorn

# Create an instance of the FastAPI application
app = FastAPI()

# Create an empty list to store the user objects
users: List[User] = []


# Define an HTTP GET endpoint for the "/status" path
@app.get(
    "/api/status",
    status_code=HTTPStatus.OK,
    response_model=AppStatus
)
def status() -> AppStatus:
    return AppStatus(users=bool(users))


# Define an HTTP GET endpoint for the "/api/users/{user_id}" path
@app.get("/api/users/{user_id}", status_code=HTTPStatus.OK)
def get_user(user_id: int) -> User:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")
    if user_id > len(users):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return users[user_id - 1]


@app.get(
    "/api/users/",
    status_code=HTTPStatus.OK,
    response_model=Page[User]
)
def get_users() -> Page[User]:
    try:
        return paginate(users)
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Add pagination support to the FastAPI application
add_pagination(app)

if __name__ == "__main__":
    with open("users.json") as f:
        users = json.load(f)

    for user in users:
        User.model_validate(user)

    print("Users loaded")

    uvicorn.run(app, host="localhost", port=8002)
