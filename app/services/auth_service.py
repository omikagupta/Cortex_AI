from sqlalchemy.orm import Session

from fastapi import HTTPException,status

from app.repositories import UserRepository
from app.core.security import (
    verify_password,
    create_access_token
)


class AuthService:


    def __init__(self):

        self.repository = UserRepository()



    def login(
        self,
        db: Session,
        email: str,
        password: str
    ):


        user = self.repository.get_by_email(
            db,
            email
        )


        if not user:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )


        if not verify_password(
            password,
            user.password_hash
        ):

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )


        token = create_access_token(
            {
                "sub": str(user.id)
            }
        )


        return token