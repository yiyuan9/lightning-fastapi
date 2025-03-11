from sqlmodel import SQLModel, Relationship, Field  # noqa: F401
from uuid import UUID
from app.models.base_models.SMSCodeRecordBase import SMSCodeRecordBase
from app.models.base_models.TodoBase import TodoBase
from app.models.base_models.UserBase import UserBase


# 用户表
class User(UserBase, table=True):
    """用户表,包含用户基本信息和关联的待办事项"""

    todos: list["Todo"] = Relationship(back_populates="user")


# 短信发送记录
class SMSCodeRecord(SMSCodeRecordBase, table=True):
    pass


# 待办事项
class Todo(TodoBase, table=True):
    """待办事项表,关联到具体用户"""

    user_id: UUID = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="todos")
