from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pymysql
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine("mysql+pymysql://user:password@localhost/database")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    description = Column(String(200), index=True)


Base.metadata.create_all(bind=engine)


# Create
@app.post("/items/")
async def create_item(item: Item):
    session = SessionLocal()
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


# Read
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    session = SessionLocal()
    item = session.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


# Update
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    session = SessionLocal()
    item_to_update = session.query(Item).filter(Item.id == item_id).first()
    if item_to_update is None:
        raise HTTPException(status_code=404, detail="Item not found")
    item_to_update.name = item.name
    item_to_update.description = item.description
    session.commit()
    session.refresh(item_to_update)
    return item_to_update


# Delete
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    session = SessionLocal()
    item_to_delete = session.query(Item).filter(Item.id == item_id).first()
    if item_to_delete is None:
        raise HTTPException(status_code=404, detail="Item not found")
    session.delete(item_to_delete)
    session.commit()
    return {"message": "Item deleted"}
