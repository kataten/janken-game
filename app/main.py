from fastapi import FastAPI, Request
from app.database import engine, Base
from app.routers import game, auth
from app.models import game as models
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Janken Web App")
app.include_router(game.router)
app.include_router(auth.router)

@app.get("/")  # ブラウザで一番最初に開く場所
def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/top")
def get_top_page(request: Request):
    return templates.TemplateResponse("top.html", {"request": request})

@app.get("/select")
def get_select_page(request: Request):
    return templates.TemplateResponse("select.html", {"request": request})

@app.get("/result_page") # 判定結果を表示する画面
def get_result_page(request: Request):
    return templates.TemplateResponse("result.html", {"request": request})

@app.get("/history_page") # 集計を表示する画面
def get_history_page(request: Request):
    return templates.TemplateResponse("history.html", {"request": request})