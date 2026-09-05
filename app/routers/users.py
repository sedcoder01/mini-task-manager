from typing import Annotated
from fastapi import APIRouter, Depends, Body
from starlette import status
from app.crud import UpdatePassword, UpdateUserPassword, UpdateUserRole, createUser, getAllUsers, getUserByEmail, getUserById, deleteUser, authenticateUser, updateUserInfo
from app.database import get_db
from app.schemas import ChangePassword, ChangeRole, CreateUser, UpdateUser, UserResponse, Token
from sqlalchemy.orm import Session
from app.dependencies import get_current_user, require_role
from fastapi.security import OAuth2PasswordRequestForm
from app.models import Role, Users

router = APIRouter(
    prefix='/user',
    tags=['user']
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[Users,Depends(get_current_user)]

@router.get('/me', status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_current_user_info(user: user_dependency):
    return user

@router.post('/createuser',status_code=status.HTTP_201_CREATED,response_model=UserResponse)
async def create_user(
    request: CreateUser,
    db: db_dependency,
    user: Users = Depends(require_role(Role.admin))):
    return createUser(request,db)

@router.post('/login',status_code=status.HTTP_200_OK,response_model=Token)
async def login_user(request : Annotated[OAuth2PasswordRequestForm,Depends()], db : db_dependency):
    return authenticateUser(request.username.lower(), request.password, db)

@router.get('/users', status_code=status.HTTP_200_OK,response_model=list[UserResponse])
async def get_all_users(
    db: db_dependency,
    user: Users = Depends(require_role(Role.admin))
):
    return getAllUsers(db)

@router.get('/{user_id}',status_code=status.HTTP_200_OK,response_model=UserResponse)
async def get_user_by_id(
    user_id: int,
    db: db_dependency,
    user: Users = Depends(require_role(Role.admin)) 
):
    return getUserById(user_id,db)

@router.get('/email/{email}',status_code=status.HTTP_200_OK,response_model=UserResponse)
async def get_user_by_email(
    email: str,
    db: db_dependency,
    user: Users = Depends(require_role(Role.admin))    
):
    return getUserByEmail(email.lower(),db)

@router.put('/user/{user_id}', status_code=status.HTTP_200_OK, response_model=UserResponse)
async def update_user_info(
    user_id: int,
    request: UpdateUser,
    db: db_dependency,
    user: Users = Depends(require_role(Role.admin))
):
    return updateUserInfo(user_id,request.name,request.email.lower(),db)

@router.patch('/{user_id}/role', status_code= status.HTTP_200_OK, response_model=UserResponse)
async def update_user_role(
    user_id: int,
    request : ChangeRole,
    db: db_dependency,
    user: Users = Depends(require_role(Role.admin))    
):
    return UpdateUserRole(user_id, request, db)

@router.patch('/password/{user_id}', status_code=status.HTTP_200_OK, response_model=UserResponse)
async def change_user_password(
    user_id: int,
    db: db_dependency,
    new_password: str = Body(min_length=5),
    user: Users = Depends(require_role(Role.admin))
):
    return UpdateUserPassword(user_id, new_password, db)

@router.patch('/me/password', status_code=status.HTTP_200_OK, response_model=UserResponse)
async def change_user_password(
    request: ChangePassword,
    db: db_dependency,
    user: user_dependency
):
    return UpdatePassword(request, db, user)

@router.delete('/{user_id}', status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, db: db_dependency, user: Users = Depends(require_role(Role.admin))):
    return deleteUser(user_id,db)