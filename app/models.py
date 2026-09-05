from app.database import Base
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer,DateTime, Enum as SQLEnum, ForeignKey,Date
from enum import Enum
import jdatetime

class Status(str, Enum):
    todo = 'todo'
    in_progress = 'in_progress'
    done = 'done'
    
class Priority(str,Enum):
    low = 'low'
    medium = 'medium'
    high = 'high'
    
class Role(str,Enum):
    admin = 'admin'
    manager = 'manager'
    user = 'user'

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer,autoincrement=True, primary_key=True, index=True)
    name = Column(String,nullable=False)
    email = Column(String,nullable=False,unique=True)
    password_hash = Column(String,nullable=False)
    role = Column(SQLEnum(Role),nullable=False,default=Role.user)
    create_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    create_at_shamsi = Column(String,default=lambda: jdatetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),nullable=False)
    
class Tasks(Base):
    __tablename__ = 'tasks'
    id = Column(Integer,autoincrement=True,primary_key=True, index=True)
    title = Column(String,nullable=False)
    description = Column (String, nullable=False)
    status = Column(SQLEnum(Status), nullable=False)
    priority = Column(SQLEnum(Priority), nullable=False)
    due_date = Column(Date,nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    create_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    update_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate= lambda: datetime.now(timezone.utc), nullable=False)
    