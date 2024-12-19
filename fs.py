from fastapi import FastAPI, Path, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Объект Jinja2Templates и папка для шаблонов
templates = Jinja2Templates(directory="templates")

# Модель пользователя
class User(BaseModel):
    id: int
    username: str
    age: int

# Список пользователей
users: List[User] = []

# Главная страница с отображением всех пользователей
@app.get("/", response_class=HTMLResponse)
def get_all_users(request: Request):
    return templates.TemplateResponse(
        "users.html", {"request": request, "users": users}
    )

# Получение информации о пользователе по ID
@app.get("/user/{user_id}", response_class=HTMLResponse)
def get_user_by_id(request: Request, user_id: int = Path(..., description="Enter User ID")):
    user = next((user for user in users if user.id == user_id), None)
    if not user:
        return templates.TemplateResponse(
            "users.html", {"request": request, "error": f"User {user_id} not found"}
        )
    return templates.TemplateResponse(
        "users.html", {"request": request, "user": user}
    )

# Добавление нового пользователя
@app.post("/user/{username}/{age}")
def create_user(username: str, age: int):
    user_id = users[-1].id + 1 if users else 1
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)
    return new_user
