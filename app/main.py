from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.routers.users import router as userRouter
from app.routers.tasks import router as taskRouter

app = FastAPI()
app.include_router(userRouter)
app.include_router(taskRouter)


@app.get('/')
async def all():
    return { "message": "Mini Task Management API" }

@app.get('/health')
async def helth():
    return { "status": "ok" }

@app.get('/health/db')
async def db_health(db: Session= Depends(get_db)):
    query = db.execute(text('Select 1'))
    if query.scalar() == 1:
        return { "database": "ok" }
    else:
        return { 'database' : 'error'}
    

