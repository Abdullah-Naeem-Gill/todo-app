from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database, auth

router = APIRouter()

@router.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(database.SessionLocal)):
    hashed_password = auth.hash_password(user.password)
    db_user = models.User(name=user.name, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login")
def login(user: schemas.UserCreate, db: Session = Depends(database.SessionLocal)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not auth.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = auth.create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/tasks", response_model=list[schemas.Task])
def get_tasks(db: Session = Depends(database.SessionLocal)):
    return db.query(models.Task).filter(models.Task.created_by == 1).all()  # Replace '1' with user ID

@router.put("/task/{task_id}/status")
def update_task_status(task_id: int, status: str, db: Session = Depends(database.SessionLocal)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task:
        task.status = status
        db.commit()
        return {"message": "Task status updated successfully"}
    raise HTTPException(status_code=404, detail="Task not found")
