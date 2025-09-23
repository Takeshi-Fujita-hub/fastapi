import os
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic import BaseModel

# 環境変数から接続情報を取得（CloudFormation で渡す）
DATABASE_URL = os.getenv("DATABASE_URL")

# DB 接続設定
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemy モデル
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

# Pydantic スキーマ
class ItemSchema(BaseModel):
    name: str

    class Config:
        orm_mode = True

Base.metadata.create_all(bind=engine)

# FastAPI アプリ本体
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI on 2025/09/23"}

@app.get("/healthz")
def health_check():
    return {"status": "ok"}

@app.post("/items/", response_model=ItemSchema)
def create_item(item: ItemSchema):
    db = SessionLocal()
    try:
        new_item = Item(name=item.name)
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    finally:
        db.close()
    return new_item

@app.get("/items/")
def read_items():
    db = SessionLocal()
    try:
        items = db.query(Item).all()
    finally:
        db.close()
    return items
