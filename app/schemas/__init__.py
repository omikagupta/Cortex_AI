from app.schemas.user import UserCreate, UserResponse

__all__ = [
    "UserCreate",
    "UserResponse",
]
from sqlalchemy.orm import Session

from app.models import User


class UserRepository:


    def get_by_email(
        self,
        db: Session,
        email: str
    ):

        return (
            db.query(User)
            .filter(
                User.email == email
            )
            .first()
        )
        from app.schemas.user import (
    UserCreate,
    UserResponse,
)

from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
)


__all__ = [
    "UserCreate",
    "UserResponse",
    "LoginRequest",
    "TokenResponse",
]