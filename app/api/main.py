from fastapi import APIRouter
from app.api.routes import login, user, todo

api_router = APIRouter()

api_router.include_router(user.router, prefix="/user", tags=["用户"])
api_router.include_router(login.router, prefix="/login", tags=["登录"])
api_router.include_router(todo.router, prefix="/todo", tags=["待办事项"])
