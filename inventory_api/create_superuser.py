import os
from getpass import getpass
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User
from dependencies import hash_password
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv("SQLALCHEMY_DATABASE_URL")
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_superuser():
    db = SessionLocal()
    username = input("Enter superuser username: ")
    password = getpass("Enter superuser password: ")
    hashed_password = hash_password(password)
    superuser = User(username=username, hashed_password=hashed_password, role="admin")
    db.add(superuser)
    db.commit()
    print("Superuser created successfully.")


if __name__ == "__main__":
    create_superuser()
