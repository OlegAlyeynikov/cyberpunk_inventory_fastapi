from inventory_api.database import engine
from inventory_api.models import Base


def create_tables():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_tables()
