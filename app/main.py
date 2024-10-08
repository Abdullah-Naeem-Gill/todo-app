from fastapi import FastAPI
from app import models, database
from .routers import admin, user

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(user.router, prefix="/user", tags=["user"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the ToDo application"}
