import models
from database import engine
from fastapi import FastAPI
from Routers import auth, todos

app = FastAPI()
# Create the database using below command at the terminal:
# createdb -U postgres -h localhost -p 5432 todoapp;
models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
# app.include_router(admin.router)
# app.include_router(users.router)
