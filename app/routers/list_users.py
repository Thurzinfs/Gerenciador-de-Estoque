from fastapi import APIRouter, Depends, HTTPException
from app.db.database import get_session
from app.models.model_user import User
from app.schemas.public.user_public import userPublic
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from typing import List

routers = APIRouter(prefix='/routers', tags=['routers'])

@routers.get(
    path='/users',
    response_model=List[userPublic]
)
def list_users(
    session: Session = Depends(get_session)
):
    database = session.query(User).all()
    return database
