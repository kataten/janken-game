from fastapi import APIRouter
import random

router = APIRouter()

@router.get("/janken/{player_hand}")
def janken(player_hand: int):
    # 0:グー, 1:チョキ, 2:パー
    cpu_hand = random.randint(0, 2)
    
    # ここで勝ち負けを判定したい！
    if player_hand == cpu_hand:
        result = "あいこ"
    # ここから下に「勝ち」と「負け」のパターンを追加したい..
    elif (player_hand - cpu_hand+3)%3 == 2:
        result = "勝ち"
    
    else:
        result = "負け"
    
    return {
        "player": player_hand,
        "cpu": cpu_hand,
        "result": result
    }