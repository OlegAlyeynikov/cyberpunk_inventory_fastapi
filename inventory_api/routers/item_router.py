from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from inventory_api import crud, schemas
from inventory_api.dependencies import get_current_user, get_db

item_router = APIRouter(
    responses={404: {"description": "Item not found"}},
)


@item_router.post("/", response_model=schemas.Item, status_code=status.HTTP_201_CREATED)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db), _: dict = Depends(get_current_user)):
    db_item = crud.create_item(db=db, item=item)
    return db_item


@item_router.get("/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@item_router.get("/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@item_router.put("/{item_id}", response_model=schemas.Item)
def update_item(item_id: int, item: schemas.ItemUpdate, db: Session = Depends(get_db)
                , _: dict = Depends(get_current_user)):
    db_item = crud.update_item(db=db, item_id=item_id, item=item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@item_router.delete("/{item_id}", response_model=schemas.Item)
def delete_item(item_id: int, db: Session = Depends(get_db), _: dict = Depends(get_current_user)):
    db_item = crud.delete_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item
