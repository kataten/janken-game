from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import random

from app.database import get_db
from app.models.game import Result

router = APIRouter()

@router.get("/janken/{player_id}/{player_hand}")
def janken(player_id: int, player_hand: int, db: Session = Depends(get_db)):
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
        player_id = player_id,
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
    
@router.get("/history/{player_id}")
def get_history(player_id: int,page: int = 1, db: Session = Depends(get_db)):
    
    per_page = 10
    skip = (page - 1) * per_page
    
    total_count = db.query(Result).filter(Result.player_id == player_id).count()
    
   # 指定されたページ分のデータだけ取得（最新順）
    results = db.query(Result).filter(Result.player_id == player_id)\
                .order_by(Result.id.desc())\
                .offset(skip).limit(per_page).all()
                
    # 2. 判定結果に合わせた変換辞書
    hand_names = {0: "グー", 1: "チョキ", 2: "パー"}
    result_names = {0: "あいこ", 1: "負け", 2: "勝ち"}
    
    #集計用の計算
    all_results = db.query(Result).filter(Result.player_id == player_id).all()
    total = len(all_results)
    wins = len([r for r in all_results if r.result == 2])
    win_rate = round(wins / total * 100,1) if total > 0 else 0

    formatted_history = []
    for r in results:
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
        "current_page":page,
        "total_pages":(total_count + per_page -1) // per_page,
        "history": formatted_history
        }