from contextlib import contextmanager
from typing import Any

from sqlalchemy import Column, DateTime, Integer, create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from api.entities import RequestStatus
from api.exceptions import StatusNotFoundError
from api.storage.abstract import Storage
from api.types import Sequence
from config import DATABASE_URL


class SessionScope:
    def __init__(self) -> None:
        self._engine = create_engine(DATABASE_URL)
        self._session_provider = sessionmaker(self._engine)

    @contextmanager
    def __call__(self, *args, commit_on_exit: bool = True, **kwargs) -> Session:
        session = self._session_provider()
        try:
            yield session
        except SQLAlchemyError:
            session.rollback()
            raise
        else:
            if commit_on_exit:
                session.commit()
        finally:
            session.close()


Base = declarative_base()  # type: Any


class FibonacciNumber(Base):
    __tablename__ = "fibonacci_numbers"

    index = Column(Integer, primary_key=True)
    value = Column(Integer, nullable=False)

    def __init__(self, index: int, value: int):
        self.index = index
        self.value = value


class RequestedCalculations(Base):
    __tablename__ = "request_statuses"

    fibo_idx = Column(Integer, primary_key=True)
    calculated_numbers = Column(Integer, nullable=False)
    requested_at = Column(DateTime, nullable=False)
    eta = Column(DateTime, nullable=False)


class DbStorage(Storage):
    def __init__(self) -> None:
        self._session_scope = SessionScope()

    def get_sequence(self, up_to_idx: int) -> Sequence:
        with self._session_scope() as session:
            sequence = (
                session.query(FibonacciNumber.index, FibonacciNumber.value)
                .filter(FibonacciNumber.index < up_to_idx)
                .order_by(FibonacciNumber.index)
                .all()
            )

        return sequence

    def get_status(self, length: int) -> RequestStatus:
        with self._session_scope() as session:
            try:
                raw_row = (
                    session.query(RequestedCalculations)
                    .filter(RequestedCalculations.fibo_idx == length)
                    .one()
                )
            except NoResultFound:
                raise StatusNotFoundError()

            request_status = RequestStatus(
                raw_row.fibo_idx, raw_row.calculated_numbers, raw_row.requested_at, raw_row.eta,
            )

        return request_status

    def save_status(self, status: RequestStatus) -> None:
        row = RequestedCalculations(
            fibo_idx=status.length,
            calculated_numbers=status.calculated_numbers,
            requested_at=status.requested_at,
            eta=status.eta,
        )
        with self._session_scope() as session:
            session.merge(row)
