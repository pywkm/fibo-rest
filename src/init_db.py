from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.config import DATABASE_URL
from api.storage.db import Base, FibonacciNumber

if __name__ == "__main__":
    engine = create_engine(DATABASE_URL)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    session.add(FibonacciNumber(0, 0))
    session.add(FibonacciNumber(1, 1))
    session.commit()
