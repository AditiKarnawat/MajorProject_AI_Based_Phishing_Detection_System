from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_token
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)

def get_current_user(
    db: Session = Depends(get_db),
    token: Optional[str] = Depends(oauth2_scheme)
) -> Optional[User]:
    """Return user object if valid token present, else None (allows anonymous scanning or authenticated scanning)."""
    if not token:
        return None
    email = decode_token(token)
    if not email:
        return None
    user = db.query(User).filter(User.email == email).first()
    return user

def require_current_user(
    current_user: Optional[User] = Depends(get_current_user)
) -> User:
    """Require authenticated user for protected routes."""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials were not provided or valid token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user
