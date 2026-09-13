from typing import Annotated

from fastapi import APIRouter, Depends, status
from app.crud import GetCurrentTask, GetNextTask, GetTasksByPriority, GetTasksByStatus, UpdateTaskDuedate, UpdateTaskInformation, UpdateTaskOwner, UpdateTaskPriority, UpdateTaskStatus, getAllTasks,CreateTaskById,GetTaskById,DeleteTasksById
from app.database import get_db
from app.dependencies import get_current_user
from app.models import Priority, Status, Users, Role
from app.schemas import CreateTask,TaskResponse, UpdateDueDate, UpdatePriority, UpdateStatus, UpdateTaskInfo
from sqlalchemy.orm import Session
from app.dependencies import user_dependency, db_dependency, require_role


router = APIRouter(
    prefix='/task',
    tags=['task']
)
user_dependency = Annotated[Users,Depends(get_current_user)]
db_dependency = Annotated[Session, Depends(get_db)]

@router.get('/all', status_code=status.HTTP_200_OK,response_model=list[TaskResponse])
async def get_all_tasks(db: db_dependency,user: user_dependency):
    return getAllTasks(db,user)

@router.get('/next', status_code=status.HTTP_200_OK,response_model=TaskResponse)
async def get_next_task(
  db : db_dependency,
  user: user_dependency  
):
    return GetNextTask(db,user)

@router.get('/uid/{user_id}', status_code=status.HTTP_200_OK,response_model=list[TaskResponse])
async def get_user_tasks_by_id(
    user_id: int,
    db: db_dependency,
    user: Users = Depends(require_role(Role.manager, Role.admin))):    
    return getAllTasks(db, user, user_id)

@router.get('/currenttask', status_code=status.HTTP_200_OK, response_model=TaskResponse)
async def get_current_task(
    db: db_dependency,
    user: user_dependency
):
    return GetCurrentTask(db, user)

@router.get('/status/', status_code=status.HTTP_200_OK, response_model=list[TaskResponse])
async def get_tasks_by_status(
    task_status: Status,
    db : db_dependency,
    user : user_dependency
):
    return GetTasksByStatus(task_status,db,user)

@router.get ('/priority', status_code=status.HTTP_200_OK, response_model=list[TaskResponse])
async def get_tasks_by_priority(
    task_priority: Priority,
    db: db_dependency,
    user: user_dependency
):
    return GetTasksByPriority(task_priority,db,user)

@router.get('/{task_id}', status_code=status.HTTP_200_OK,response_model=TaskResponse)
async def get_task_by_id(task_id : int ,db: db_dependency, user: user_dependency):
    return GetTaskById(task_id,user, db)

@router.post('/create_task', status_code= status.HTTP_201_CREATED, response_model=TaskResponse)
async def create_task(
    request : CreateTask,
    db: db_dependency,
    user: Users = Depends(require_role(Role.admin,Role.manager)) ,
    ):
    return CreateTaskById(request, db)

@router.patch('/info/{task_id}', status_code=status.HTTP_200_OK,response_model=TaskResponse)
async def update_task_info(
    task_id: int,
    info: UpdateTaskInfo,
    db: db_dependency,
    user: Users = Depends(require_role(Role.admin,Role.manager))
):
    return UpdateTaskInformation(task_id, info, db)

@router.patch('/priority/{task_id}', status_code=status.HTTP_200_OK, response_model=TaskResponse)
async def update_task_status(
    request: UpdatePriority,
    task_id: int,
    db: db_dependency,
    user: Users = Depends(require_role(Role.admin,Role.manager))
):
    return UpdateTaskPriority(request,task_id,db,user)

@router.patch('/due_date/{task_id}', status_code=status.HTTP_200_OK, response_model=TaskResponse)
async def update_task_duedate(
    request: UpdateDueDate,
    task_id: int,
    db: db_dependency,
    user: Users = Depends(require_role(Role.admin,Role.manager))
):
    return UpdateTaskDuedate(request,task_id,db,user)

@router.patch('/status/{task_id}', status_code=status.HTTP_200_OK, response_model=TaskResponse)
async def update_task_status(
    request: UpdateStatus,
    task_id: int,
    db: db_dependency,
    user: user_dependency
):
    return UpdateTaskStatus(request,task_id,db,user)

@router.patch('/owner/{task_id}', status_code=status.HTTP_200_OK,response_model=TaskResponse)
async def update_task_owner(
    task_id: int,
    owner_id: int,
    db: db_dependency,
    user: Users = Depends(require_role(Role.admin, Role.manager))
):
    return UpdateTaskOwner(task_id,owner_id,db)



@router.delete('/{task_id}', status_code=status.HTTP_200_OK)
async def delete_task_by_id(
    task_id : int,
    db: db_dependency,
    user: Users = Depends(require_role(Role.admin, Role.manager))    
):
    return DeleteTasksById(task_id, db)

