from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Generator

from app.db.schema import session_local
from app.models.user import UserCreate, UserRead
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


# SQLAlchemy 2.0 best practice: Dependency with proper cleanup
def get_db() -> Generator[Session, None, None]:
    """Database session dependency with automatic cleanup."""
    db = session_local()
    try:
        yield db
    finally:
        db.close()


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    """User service dependency."""
    return UserService(session=db)


@router.get("", response_model=list[UserRead])
def get_users(service: UserService = Depends(get_user_service)):
    return service.list_users()


@router.post("", response_model=UserRead)
def create_user(user: UserCreate, service: UserService = Depends(get_user_service)):
    return service.create_user(user.name)


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, service: UserService = Depends(get_user_service)):
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int, user: UserCreate, service: UserService = Depends(get_user_service)
):
    updated = service.update_user(user_id, user.name)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated


@router.delete("/{user_id}")
def delete_user(user_id: int, service: UserService = Depends(get_user_service)):
    success = service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"success": True}
