from typing import List

from sqlmodel import Session, select

from app.models.table import Todo


class TodoCRUD:
    def __init__(self, session: Session):
        self.session = session

    def get_all_todos(self, user_id: str) -> List[Todo]:
        """获取所有未删除的待办事项"""
        stmt = select(Todo).where(
            Todo.is_deleted == False, Todo.user_id == user_id  # noqa: E712
        )  # Filter by user ID
        return self.session.exec(stmt).all()

    def get_completed_todos(self, user_id: str) -> List[Todo]:
        """获取所有已完成的待办事项"""
        stmt = select(Todo).where(
            Todo.is_deleted == False,  # noqa: E712
            Todo.completed == True,  # noqa: E712
            Todo.user_id == user_id,  # Filter by user ID
        )
        return self.session.exec(stmt).all()

    def get_todo(self, todo_id: str) -> Todo | None:
        """根据ID获取待办事项"""
        return self.session.get(Todo, todo_id)

    def create_todo(self, text: str, user_id: str) -> Todo:
        """创建新的todo"""
        new_todo = Todo(text=text, user_id=user_id)
        print(f"Creating todo: {new_todo}")  # Print the new todo details
        self.session.add(new_todo)
        self.session.commit()
        self.session.refresh(new_todo)
        return new_todo

    def complete_todo(self, todo_id: str, user_id: str) -> Todo | None:
        """将待办事项标记为已完成"""
        todo = self.get_todo(todo_id)
        if not todo or todo.user_id != user_id:  # Check if todo belongs to user
            return None

        todo.completed = True
        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)
        return todo

    def delete_todo(self, todo_id: str, user_id: str) -> bool:
        """软删除待办事项"""
        todo = self.get_todo(todo_id)
        if not todo or todo.user_id != user_id:  # Check if todo belongs to user
            return False

        todo.is_deleted = True
        self.session.add(todo)
        self.session.commit()
        return True
