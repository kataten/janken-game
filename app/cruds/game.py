from sqlalchemy.orm import Session
from models import game as models
from sqlalchemy import desc

def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).get(user_id)

def create_user(db: Session, user_data: dict):
    db_user = models.User(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_result(db: Session, result_data: dict):
    db_res = models.Result(**result_data)
    db.add(db_res)
    db.commit()
    return db_res

def get_user_stats(db: Session, user_id: int):
    all_res = db.query(models.Result).filter(models.Result.player_id == user_id).all()
    recent = db.query(models.Result).filter(models.Result.player_id == user_id).order_by(desc(models.Result.created_at)).limit(10).all()
    return all_res, recent