from fastapi import APIRouter, Body, HTTPException

from app.api.depends import CurrentUser, SessionDep
from app.crud.TodoCRUD import TodoCRUD

router = APIRouter()


@router.get("/all", summary="查询全部待办事项")
def get_all_todos(session: SessionDep, user: CurrentUser):
    return TodoCRUD(session).get_all_todos(user.id)


@router.post("/add", summary="添加todo")
def add_todo(session: SessionDep, user: CurrentUser, text: str = Body(embed=True)):
    TodoCRUD(session).create_todo(text, user.id)
    return ""


@router.put("/complete", summary="完成待办事项")
def complete_todo(
    session: SessionDep, user: CurrentUser, todo_id: str = Body(embed=True)
):
    todo = TodoCRUD(session).complete_todo(todo_id, user.id)
    if not todo:
        raise HTTPException(status_code=404, detail="待办事项不存在或不属于该用户")
    return todo


@router.delete("/delete", summary="删除待办事项")
def delete_todo(
    session: SessionDep, user: CurrentUser, todo_id: str = Body(embed=True)
):
    success = TodoCRUD(session).delete_todo(todo_id, user.id)
    if not success:
        raise HTTPException(status_code=404, detail="待办事项不存在或不属于该用户")
    return {"message": "删除成功"}


@router.get("/completed", summary="查询已完成待办事项")
def get_completed_todos(session: SessionDep, user: CurrentUser):
    return TodoCRUD(session).get_completed_todos(user.id)
