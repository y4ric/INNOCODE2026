from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import sys
from pathlib import Path

frontend_root = str(Path(__file__).resolve().parent.parent)
if frontend_root not in sys.path:
    sys.path.append(frontend_root)


from database import get_db
from models.user import User, UserRole
from schemas.user import UserResponse
from services.user_service import UserService

router = APIRouter(tags=["users"])


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)


@router.get(
    "/users/me",
    response_model=UserResponse,
)
def get_my_user(current_user: User = Depends(get_current_user)):
    return current_user


@router.get(
    "/admin/users",
    response_model=list[UserResponse],
)
def get_admin_users(
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    service: UserService = Depends(get_user_service),
):
    return service.get_users()