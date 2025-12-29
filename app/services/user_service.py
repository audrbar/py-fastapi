from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.schema import User


class UserService:
    """User service using SQLAlchemy 2.0 style queries."""

    def __init__(self, session: Session):
        self._db = session

    def list_users(self) -> list[User]:
        """Get all users using modern select() API."""
        stmt = select(User)
        return list(self._db.scalars(stmt).all())

    def get_user(self, user_id: int) -> User | None:
        """Get user by ID using modern select() API."""
        stmt = select(User).where(User.id == user_id)
        return self._db.scalars(stmt).first()

    def create_user(self, name: str) -> User:
        user = User(name=name)
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)
        return user

    def update_user(self, user_id: int, name: str) -> User | None:
        user = self.get_user(user_id)
        if not user:
            return None
        user.name = name
        self._db.commit()
        self._db.refresh(user)
        return user

    def delete_user(self, user_id: int) -> bool:
        user = self.get_user(user_id)
        if not user:
            return False
        self._db.delete(user)
        self._db.commit()
        return True
