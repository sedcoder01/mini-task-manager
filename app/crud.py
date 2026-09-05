from fastapi import HTTPException, Path
from sqlalchemy.exc import IntegrityError
from app.models import Role, Users, Tasks, Status,Priority
from app.schemas import ChangePassword, ChangeRole, CreateTask,UpdateTask,CreateUser, UpdateTaskStatus
from datetime import datetime, timezone
from app.security import hash_password,verify_password, create_access_token




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

def UpdateUserPassword(user_id: int, request: str, db):
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
    if request.due_date <= datetime.now(timezone.utc).date():
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
    return task

def GetTaskById(task_id: int, user, db):
    task = db.query(Tasks).filter(Tasks.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail='Task Not Found')
    if user.role == Role.user and task.user_id != user.id:
        raise HTTPException(status_code=403,detail='You do not have permission to access this task')
    return task

def GetTasksByUserId(user_id: int, db):
    tasks = db.query(Tasks).filter(Tasks.user_id == user_id).all()
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
    task.title = request.title
    task.description = request.description
    task.status = request.status
    task.priority = request.priority
    task.due_date = request.due_date
    task.user_id = request.user_id
    db.commit()
    db.refresh(task)
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
    return task

def DeleteTasksById(task_id: int, db):
    task = db.query(Tasks).filter(Tasks.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail='Task Not Found')
    db.query(Tasks).filter(Tasks.id == task_id).delete()
    db.commit()
    return 'DONE'