from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database, auth

router = APIRouter()

@router.post("/create-user", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.SessionLocal)):
    hashed_password = auth.hash_password(user.password)
    db_user = models.User(name=user.name, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users", response_model=list[schemas.User])
def get_all_users(db: Session = Depends(database.SessionLocal)):
    return db.query(models.User).all()

@router.post("/assign-task")
def assign_task(task_id: int, user_id: int, db: Session = Depends(database.SessionLocal)):
    task_assignment = models.TaskAssignment(task_id=task_id, user_id=user_id)
    db.add(task_assignment)
    db.commit()
    return {"message": "Task assigned successfully"}

@router.delete("/unassign-task/{task_id}/{user_id}")
def unassign_task(task_id: int, user_id: int, db: Session = Depends(database.SessionLocal)):
    task_assignment = db.query(models.TaskAssignment).filter(
        models.TaskAssignment.task_id == task_id, 
        models.TaskAssignment.user_id == user_id
    ).first()
    if task_assignment:
        db.delete(task_assignment)
        db.commit()
        return {"message": "Task unassigned successfully"}
    raise HTTPException(status_code=404, detail="Task assignment not found")
