from datetime import datetime, date
from app.models import Status, Priority, Role
from pydantic import Field, EmailStr, BaseModel, ConfigDict

class CreateUser(BaseModel):
    name: str = Field(min_length=1, max_length=30)
    email: EmailStr=Field(min_length=3)
    password: str = Field(min_length=5)
    role: Role = Field(default=Role.user)
    
class UpdateUser(BaseModel):
    name: str = Field(min_length=1, max_length=30)
    email: EmailStr=Field(min_length=3)

class ChangeRole(BaseModel):
    role: Role = Field(default=Role.user)
    
class ChangePassword(BaseModel):
    old_password: str = Field(min_length=5)
    new_password: str = Field(min_length=5)
    
class LoginUser(BaseModel):
    email: EmailStr
    password : str

class UserResponse(BaseModel):
    id : int
    name: str
    email : EmailStr
    role : str
    create_at : datetime
    model_config = ConfigDict(from_attributes=True)
    
class CreateTask(BaseModel):
    title : str = Field(min_length=1)
    description : str = Field(min_length=3)
    status : Status = Field()
    priority : Priority = Field()
    due_date : date = Field()
    user_id : int = Field(gt=0)
    
class UpdateTask(BaseModel):
    title : str = Field(min_length=1)
    description : str = Field(min_length=3)
    status : Status = Field()
    priority : Priority = Field()
    due_date : date = Field()
    user_id : int = Field(gt=0)
    
class UpdateTaskStatus(BaseModel):
    status : Status

class TaskResponse(BaseModel):
    id : int
    title: str
    description : str
    status : Status
    priority : Priority
    due_date : date
    user_id : int
    create_at : datetime
    update_at : datetime
    model_config = ConfigDict(from_attributes=True)
    
class Token(BaseModel):
    access_token: str
    token_type: str