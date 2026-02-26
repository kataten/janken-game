from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import random

from app.database import get_db
from app.models.game import Result

router = APIRouter()

@router.get("/janken/{player_hand}")
def janken(player_hand: int, db: Session = Depends(get_db)):
    # 0:グー, 1:チョキ, 2:パー
    cpu_hand = random.randint(0, 2)
    
    # ここで勝ち負けを判定 0:あいこ 1:負け 2:勝ち
    if player_hand == cpu_hand:
        result_code = 0
    elif (player_hand - cpu_hand+3)%3 == 2:
        result_code = 2
    else:
        result_code = 1
        
    new_record = Result(
        player_id = 1,
        player_hand = player_hand,
        cpu_hand = cpu_hand,
        result = result_code
    )
    
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
        
    return {
        "id": new_record.id,
        "player": player_hand,
        "cpu": cpu_hand,
        "result": result_code
        
    }
    
@router.get("/history")
def get_history(db: Session = Depends(get_db)):
    # 1. DBからデータを新しい順に取得
    history = db.query(Result).order_by(Result.id.desc()).all()
    
    # 2. 判定結果に合わせた変換辞書
    hand_names = {0: "グー", 1: "チョキ", 2: "パー"}
    result_names = {0: "あいこ", 1: "負け", 2: "勝ち"}
    
    #集計用の計算
    total = len(history)
    wins = len([r for r in history if r.result == 2])
    win_rate = round(wins / total * 100,1) if total > 0 else 0

    formatted_history = []
    for r in history:
        formatted_history.append({
            "id": r.id,
            "player_id": r.player_id, 
            "player_hand": hand_names.get(r.player_hand, "不明"), 
            "cpu_hand": hand_names.get(r.cpu_hand, "不明"),       
            "result": result_names.get(r.result, "不明"),         
            "date": r.created_at.strftime("%Y/%m/%d %H:%M") if r.created_at else "不明"
        })
    
    return {
        "win_rate": f"{win_rate:.1f}%",
        "total_games":total,
        "history": formatted_history}