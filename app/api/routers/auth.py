from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from app.api.dependencies.database import get_db
from app.schemas import LoginRequest, TokenResponse
from app.services.auth_service import AuthService



router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


service = AuthService()



@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):

    token = service.login(
        db,
        data.email,
        data.password
    )


    return {
        "access_token": token
    }