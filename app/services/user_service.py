from sqlalchemy.orm import Session

from app.models import User
from app.repositories import UserRepository
from app.schemas import UserCreate


class UserService:

    def __init__(self):

        self.repository = UserRepository()

    def create_user(
        self,
        db: Session,
        user_data: UserCreate,
    ):

        user = User(
            email=user_data.email,
            password_hash=user_data.password,
            full_name=user_data.full_name,
        )

        return self.repository.create(db, user)

    def get_user(
        self,
        db: Session,
        user_id: int,
    ):
        return self.repository.get_by_id(db, user_id)