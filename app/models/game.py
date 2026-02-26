from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import datetime

class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    password = Column(String)
    results = relationship("Result", back_populates="owner")

class Result(Base):
    __tablename__ = "results"
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    player_hand = Column(Integer)  # 0:グー, 1:チョキ, 2:パー
    cpu_hand = Column(Integer)
    result = Column(Integer)        # 勝ち/負け/引き分け
    created_at = Column(DateTime, default=datetime.datetime.now)
    owner = relationship("Player", back_populates="results")