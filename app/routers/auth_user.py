from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.database import get_session
from app.models.model_user import User
from app.core.security import verify_password, create_acess_token
from app.schemas.token.schema_token import Token

auth_router = APIRouter(prefix="/auth", tags=['auth'])

@auth_router.post(
    path="/token",
    response_model=Token
)
def login_for_acess_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    user = session.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token = create_acess_token(data= {'sub' : user.email})
    return {
        'access_token' : access_token,
        'token_type' : 'Bearer'
    }
