from dotenv import load_dotenv
from fastapi import FastAPI
from inventory_api import models
from inventory_api.database import engine
from inventory_api.routers import user_router, item_router


load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router.user_router, prefix="/users")
app.include_router(item_router.item_router, prefix="/items")
