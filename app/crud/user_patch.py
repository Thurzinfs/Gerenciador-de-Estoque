from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.public.user_public import userPublic
from app.schemas.update.user_update import userUpdate
from app.db.database import get_session
from app.core.security import get_password_hash
from app.core.security import get_current_user
from http import HTTPStatus
from app.services.user_services import patch_user_service

patch_router = APIRouter(prefix='/api/users', tags=['users'])

@patch_router.patch(
    path='/{user_id}',
    response_model=userPublic
)
def update_user(
    user_id: int,
    user: userUpdate,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    data = user.model_dump(exclude_unset=True)

    return patch_user_service(
        session=session,
        user_data=data,
        user_id=user_id,
        current_user=current_user
    )