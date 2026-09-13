from fastapi import HTTPException, Path
from sqlalchemy.exc import IntegrityError
from app.models import Role, Users, Tasks, Status,Priority
from app.schemas import ChangePassword, ChangeRole, CreateTask,UpdateTask,CreateUser, UpdateTaskStatus
from datetime import datetime, timezone
from app.security import hash_password,verify_password, create_access_token
import json
from app.redis import redis_client
from fastapi.encoders import jsonable_encoder



def createUser(request: CreateUser ,db):
    user = Users(
        name=request.name,
        email=request.email.lower(),
        password_hash = hash_password(request.password),
        role=request.role,
    )
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409,detail="Email is Exist, Use A Diffrent Email")
    return user
    

def getAllUsers(db):
    users = db.query(Users).order_by(Users.id).all()
    
    return users


def getUserById(user_id: int, db):
    user = db.query(Users).filter(Users.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404,detail="User Not Found")
    return user

def getUserByEmail(email: str, db):
    user = db.query(Users).filter(Users.email == email).first()
    return user

def authenticateUser(email: str, password: str, db):
    user = getUserByEmail(email,db)
    if user is None:
        raise HTTPException(status_code=401, detail="Email or Password is Incorrect")
    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Email or Password is Incorrect")
    token = create_access_token(
        { 'sub' : str(user.id)}
    )
    return {
        'access_token': token,
        'token_type': 'bearer'
    }
    
def updateUserInfo(user_id: int,name : str,email: str, db):
    user = db.query(Users).filter(Users.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User Not Found')
    user.name = name
    user.email = email
    try:
        db.add(user)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409,detail="Email is Exist")
    return user
        
def UpdateUserRole(user_id: int, request: ChangeRole, db):
    user = db.query(Users).filter(Users.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User Not Found')
    user.role = request.role
    db.commit()
    return user

def UpdateUserPasswordById(user_id: int, request: str, db):
    user = db.query(Users).filter(Users.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User Not Found')
    user.password_hash = hash_password(request)
    db.commit()
    return user

def UpdatePassword(request: ChangePassword, db, user):
    if not verify_password(request.old_password, user.password_hash):
        raise HTTPException(status_code=400,detail="Old Password is Incorrect")
    user.password_hash = hash_password(request.new_password)
    db.commit()
    return user

def deleteUser(user_id: int, db):
    user = db.query(Users).filter(Users.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User Not Found')
    
    db.query(Users).filter(Users.id == user_id).delete()
    db.commit()
    return f'User {user.id} Deleted Successfully'

def getAllTasks(db,user):
    if user.role == Role.admin or user.role == Role.manager:
        tasks = db.query(Tasks).order_by(Tasks.id).all()
    else:
        tasks = db.query(Tasks).filter(Tasks.user_id == user.id).order_by(Tasks.id).all()
    return tasks

def CreateTaskById(request : CreateTask ,db):
    owner = db.query(Users).filter(Users.id == request.user_id).first()
    if owner is None:
        raise HTTPException(status_code=404, detail='Owner of Task Not Found')
    if request.due_date < datetime.now(timezone.utc).date():
            raise HTTPException(
            status_code=400,
            detail="Due date must be after creation date"
        )
    task = Tasks(
        title = request.title,
        description = request.description,
        status = request.status,
        priority = request.priority,
        due_date = request.due_date,
        user_id = request.user_id
    )
    db.add(task)
    db.commit()
    redis_client.rpush(
        f"tasks:queue:user:{request.user_id}",
        task.id
    )
    # redis_client.delete(f'tasks:user:{request.user_id}') //Task changed, need Rebuild
    return task

def GetTaskById(task_id: int, user, db):
    task = db.query(Tasks).filter(Tasks.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail='Task Not Found')
    if user.role == Role.user and task.user_id != user.id:
        raise HTTPException(status_code=403,detail='You do not have permission to access this task')
    return task

def GetUserTasks(user_id: int, db):
    cache_key = f'tasks:user:{user_id}'
    cached_tasks = redis_client.get(cache_key)
    if cached_tasks:
        return json.loads(cached_tasks)
    tasks = db.query(Tasks).filter(Tasks.user_id == user_id).all()
    tasks_data = jsonable_encoder(tasks)
    redis_client.set(
        cache_key,
        json.dumps(tasks_data),
        ex=60
    )
    return tasks

def UpdateTaskById(task_id : int, request : UpdateTask ,db):
    task = db.query(Tasks).filter(Tasks.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail='Task Not Found')
    owner = db.query(Users).filter(Users.id == request.user_id).first()
    if owner is None:
        raise HTTPException(status_code=404, detail='Owner of Task Not Found')
    if request.due_date <= task.create_at.date():
        raise HTTPException(
        status_code=400,
        detail="Due date must be after creation date"
    )
    old_user_id = task.user_id
    if task.user_id != request.user_id:
        redis_client.lrem(f'tasks:queue:user:{old_user_id}', 0, str(task.id))
        redis_client.lrem(f'tasks:processing:user:{old_user_id}', 0, str(task.id))
        task.user_id = request.user_id
    if request.status == Status.in_progress:
        processing_key = f'tasks:processing:user:{request.user_id}'
        if redis_client.llen(processing_key) > 0:
            request.status = Status.todo
    task.title = request.title
    task.description = request.description
    task.priority = request.priority
    task.due_date = request.due_date
    task.status = request.status
    db.commit()
    db.refresh(task)
    if task.status == Status.todo:
        redis_client.rpush(f'tasks:queue:user:{task.user_id}', task.id)
    elif task.status == Status.in_progress:
        processing_key = f'tasks:processing:user:{task.user_id}'
        redis_client.rpush(processing_key, task.id)
    # redis_client.delete(f'tasks:user:{old_user_id}')
    # redis_client.delete(f'tasks:user:{request.user_id}')
    return task

def UserUpdateTaskByID(request: UpdateTaskStatus ,task_id: int, db, user):
    task = db.query(Tasks).filter(Tasks.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task Not Found")
    if user.role == Role.user and user.id != task.user_id:
        raise HTTPException(status_code=403,detail="You do not have permission to update this task")
    task.status = request.status
    db.commit()
    db.refresh(task)
    # redis_client.delete(f'tasks:user:{user.id}')
    if request.status == Status.done:
        redis_client.lrem( #remove Item By ID not index, example processing: [5, 6, 7] lrem 6 result: [5, 7]
            f'tasks:processing:user:{task.user_id}',
            1,
            str(task.id)
        )
    return task

def DeleteTasksById(task_id: int, db):
    task = db.query(Tasks).filter(Tasks.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail='Task Not Found')
    db.query(Tasks).filter(Tasks.id == task_id).delete()
    db.commit()
    # redis_client.delete(f'tasks:user:{task.user_id}')
    redis_client.lrem(f'tasks:queue:user:{task.user_id}', 0, str(task.id))
    redis_client.lrem(f'tasks:processing:user:{task.user_id}', 0, str(task.id))
    return 'DONE'

def GetNextTask(db, user):
    queue_key = f'tasks:queue:user:{user.id}'
    proccessing_key = f'tasks:processing:user:{user.id}'
    
    processing_task = redis_client.lrange(proccessing_key, 0, 0)
    if processing_task:
        raise HTTPException(status_code=400,detail="Please complete your current task first")
    
    task_id = redis_client.lmove(
        queue_key,
        proccessing_key,
        "LEFT",
        "RIGHT"
    )
    if task_id is None:
        raise HTTPException(status_code=404, detail="No Task Available")
    task = db.query(Tasks).filter(Tasks.id == int(task_id)).first()
    if task is None:
        raise HTTPException(status_code=404,detail="Task Not Found")
    task.status = Status.in_progress
    db.commit()
    db.refresh(task)
    return task

def RebuildTaskQueues(db):
    tasks = db.query(Tasks).filter(Tasks.status != Status.done).all()
    if tasks:
        for task in tasks:
            queue_key = f'tasks:queue:user:{task.user_id}'
            processing_key = f'tasks:processing:user:{task.user_id}'
            if (
                redis_client.lpos(queue_key, str(task.id)) is not None
            or
                redis_client.lpos(processing_key, str(task.id)) is not None
            ):
                continue
            if task.status == Status.todo:
                    redis_client.rpush(queue_key, task.id)
            elif task.status == Status.in_progress:
                redis_client.rpush(processing_key, task.id)