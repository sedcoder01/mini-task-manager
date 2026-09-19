from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.routers.users import router as userRouter
from app.routers.tasks import router as taskRouter
from app.redis import redis_client
from fastapi.middleware.cors import CORSMiddleware
# from app.crud import RebuildTaskQueues

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500","http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.on_event('startup')
# def startup():
#     db = next(get_db())
#     try:
#         RebuildTaskQueues(db)
#     finally:
#         db.close()
        
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

@app.get('/redis-test')
def redis_test():
    redis_client.set('test', 'Hello Redis!')
    
    value = redis_client.get('test')
    
    return {
        'redis': value
    }

