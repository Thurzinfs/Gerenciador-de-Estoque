from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.put.user_put import userPut
from app.schemas.public.user_public import userPublic
from app.db.database import get_session
from app.core.security import get_password_hash
from app.core.security import get_current_user
from http import HTTPStatus
from app.services.user_services import update_put_user_service

put_router = APIRouter(prefix='/api/users', tags=['users'])

@put_router.put(
    path='/{user_id}',
    response_model=userPublic
)
def update_user(
    user_id: int,
    user: userPut,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    data = user.model_dump()

    return update_put_user_service(
        session=session,
        user_data=data,
        user_id=user_id,
        current_user=current_user
    )