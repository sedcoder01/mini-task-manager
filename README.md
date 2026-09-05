# Project Name
mini-task-manager
# Project Description
Initial FastAPI Task Manager
# Create Virtual Environment
mini-task-manager>python -m venv .venv
# Activate Virtual Environment
mini-task-manager> .venv/scripts/activate.bat
# Install Dependencies
(.venv) pip install fastapi
(.venv) pip install uvicorn
# Run Application
uvicorn app.main:app --reload
# Health Endpoint
GET /health --> Code : 200 OK
# Swagger UI
/docs --> Opened Successfully
# Project Structure
.venv
app
    - __init__.py
    - main.py
data
tests
# __init__.py
این فایل اگر داخل پوشه ای قرار گیرد پایتون آن پوشه را بعنوان پکیج در نظر می گیرد.
می توان کتابخانه های مربوط نیاز پکیج را در این فایل نیز فراخوانی کرد.
# Database Type
sqlite3
# Database File Location
mini-task-manager/data/task_manager.db
# SQLAlchemy
یک فریمورک جهت ارتباط با پایگاه های داده مختلف
# Engine
نقطه آغاز اتصال به پایگاه داده در فریمورک SQLAlchemy
# Session
جهت کار با ORM می بایست یک Session تعریف گردد و انجین به آن متصل گردد
# Base
هر کلاسی که از این شی ارث بری کند بعنوان جدول اصلی در دیتابیس قرار می گیرد. همچنین وظیفه تولید متادیتا ایجاد جداول را نیز انجام می دهد
# get_db()
یک Session جهت کار با دیتابیس باز می کند و بعد از اتمام عملیات نیز Session را می بندد
# Database Helth Check
یک عملیت ساده جهت تست ارتباط با دیتابیس انجام می شود و در صورت سلامت ارتباط پیغام مناسب برگشت داده می شود.
