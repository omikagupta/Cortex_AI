from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import traceback

from app.api.dependencies.database import get_db
from app.schemas import UserCreate, UserResponse
from app.services import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

service = UserService()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    try:
        return service.create_user(db, user)
    except Exception as e:
        traceback.print_exc()
        raise e