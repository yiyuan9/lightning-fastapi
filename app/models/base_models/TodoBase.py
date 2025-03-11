from sqlmodel import Field

from app.models.base_models.Base import TableBase


class TodoBase(TableBase):
    text: str = Field(
        unique=True, index=True, nullable=False, description="待办事项内容"
    )

    completed: bool = Field(default=False, description="是否已完成")
