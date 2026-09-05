from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status
from app.crud import UserUpdateTaskByID, getAllTasks,CreateTaskById,GetTaskById,GetTasksByUserId,UpdateTaskById,DeleteTasksById
from app.database import get_db
from app.dependencies import get_current_user
from app.models import Users, Role
from app.schemas import CreateTask,TaskResponse, UpdateTask, UpdateTaskStatus
from sqlalchemy.orm import Session
from app.dependencies import user_dependency, db_dependency, require_role


router = APIRouter(
    prefix='/task',
    tags=['task']
)
user_dependency = Annotated[Users,Depends(get_current_user)]
db_dependency = Annotated[Session, Depends(get_db)]

@router.get('/all', status_code=status.HTTP_200_OK,response_model=list[TaskResponse])
async def get_all_taks(db: db_dependency,user: user_dependency):
    return getAllTasks(db,user)

@router.get('/{task_id}', status_code=status.HTTP_200_OK,response_model=TaskResponse)
async def get_task_by_id(task_id : int ,db: db_dependency, user: user_dependency):
    return GetTaskById(task_id,user, db)

@router.get('/uid/{user_id}', status_code=status.HTTP_200_OK,response_model=list[TaskResponse])
async def get_task_by_user_id(
    user_id : int,
    db: db_dependency,
    user: Users = Depends(require_role(Role.manager,Role.admin))    
):
    return GetTasksByUserId(user_id, db)

@router.post('/create_task', status_code= status.HTTP_201_CREATED, response_model=TaskResponse)
async def create_task(
    request : CreateTask,
    db: db_dependency,
    user: Users = Depends(require_role(Role.admin,Role.manager)) ,
    ):
    return CreateTaskById(request, db)

@router.put('/{task_id}', status_code=status.HTTP_200_OK, response_model=TaskResponse)
async def update_task(
    request: UpdateTask,
    task_id: int,
    db: db_dependency,
    user: Users = Depends(require_role(Role.admin,Role.manager))):
    return UpdateTaskById(task_id,request, db)

@router.patch('/status/{task_id}', status_code=status.HTTP_200_OK, response_model=TaskResponse)
async def update_task_status(
    request: UpdateTaskStatus,
    task_id: int,
    db: db_dependency,
    user: user_dependency
):
    return UserUpdateTaskByID(request,task_id,db,user)

@router.delete('/{task_id}', status_code=status.HTTP_200_OK)
async def delete_task_by_id(
    task_id : int,
    db: db_dependency,
    user: Users = Depends(require_role(Role.admin, Role.manager))    
):
    return DeleteTasksById(task_id, db)