from fastapi import Depends, HTTPException, status, Cookie
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt
from app.config import settings
from app.database import get_db
from app.models import Users, Role
from typing import Annotated, TypeAlias

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='user/login')


def get_current_user(
    # access_token: Annotated[str | None, Cookie()] = None,
    bearer_token: Annotated[str | None, Depends(oauth2_scheme)] = None,
    db: Session =  Depends(get_db)
):
    token = bearer_token #or access_token 
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get('sub')
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials")
    
    user = db.query(Users).filter(Users.id == int(user_id)).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User Not Found")
    
    return user 

user_dependency: TypeAlias = Annotated[Users, Depends(get_current_user)]
db_dependency : TypeAlias = Annotated[Session, Depends(get_db)]

def require_role(*allowed_roles: Role):

    def role_checker(user: user_dependency):

        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission"
            )

        return user

    return role_checker