from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import uuid

from app.core.config import settings
from app.core.database import get_db
from app.core.security import verify_token
from app.models.user import User

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(reusable_oauth2)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    subject = verify_token(token)
    if subject is None:
        raise credentials_exception
        
    try:
        user_uuid = uuid.UUID(subject)
    except ValueError:
        # If subject is email, fetch by email
        user = db.query(User).filter(User.email == subject).first()
        if not user:
            raise credentials_exception
        return user
        
    user = db.query(User).filter(User.id == user_uuid).first()
    if not user:
        raise credentials_exception
    return user

def get_current_active_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user does not have enough privileges"
        )
    return current_user
