from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.game import Player
from pydantic import BaseModel
from app.utils import hash_password, verify_password

router = APIRouter()

# リクエストを受け取るためのデータ型定義
class UserAuth(BaseModel):
    name: str
    password: str

# --- 新規登録 ---
@router.post("/register")
def register(user: UserAuth, db: Session = Depends(get_db)):
    # すでに同じ名前のユーザーがいるかチェック
    existing_user = db.query(Player).filter(Player.name == user.name).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="既に登録されている名前です")
    
    #パスワードをハッシュ化して保存
    hashed_pwd = hash_password(user.password)
    
    new_player = Player(name=user.name, password=hashed_pwd)
    db.add(new_player)
    db.commit()
    db.refresh(new_player)
    return {"message": "登録が完了しました", "player_id": new_player.id}

# --- ログイン ---
@router.post("/login")
def login(user: UserAuth, db: Session = Depends(get_db)):
    # 名前とパスワードが一致するユーザーを探す
    db_user = db.query(Player).filter(Player.name == user.name).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="名前またはパスワードが間違っています")
    
    return {"message": "ログイン成功", "player_id": db_user.id, "name": db_user.name}