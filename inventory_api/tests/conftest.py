from fastapi.testclient import TestClient
from inventory_api.main import app
from inventory_api.dependencies import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from inventory_api.database import Base
import pytest
from sqlalchemy_utils import database_exists, create_database
import os


database_url = os.getenv("SQLALCHEMY_DATABASE_URL")
engine = create_engine(database_url)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def test_db():
    if not database_exists(database_url):
        create_database(database_url)

    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(test_db):
    def _get_test_db_override():
        try:
            yield test_db
        finally:
            test_db.close()

    app.dependency_overrides[get_db] = _get_test_db_override
    with TestClient(app) as client:
        yield client
