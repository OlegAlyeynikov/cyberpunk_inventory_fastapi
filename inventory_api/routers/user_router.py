import os
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from inventory_api import crud, schemas, dependencies
from inventory_api.dependencies import get_current_user, hash_password, verify_password, get_db
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm

user_router = APIRouter(responses={404: {"description": "User not found"}},)
token_expire = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


@user_router.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=token_expire)
    access_token = dependencies.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_pwd = hash_password(user.password)
    return crud.create_user(db=db, user=user, hashed_password=hashed_pwd)


@user_router.put("/{user_id}", response_model=schemas.User)
def update_user_endpoint(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db),
                         _: dict = Depends(get_current_user)):
    updated_user = crud.update_user(db=db, user_id=user_id, user_update=user_update)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@user_router.post("/login")
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user_credentials.username)
    if not db_user or not verify_password(user_credentials.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
