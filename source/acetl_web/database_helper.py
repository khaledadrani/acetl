from contextlib import contextmanager
from typing import Generator, ContextManager, Callable, Any

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session


class Database:
    def __init__(self, db_url: str) -> None:
        self.engine = create_engine(db_url, echo=False)
        self.session_factory = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine)
        )

    @contextmanager
    def session(self) -> Generator[Callable[..., ContextManager[Session]], Any, None]:
        session = self.session_factory()
        try:
            yield session
        except Exception as error:
            session.rollback()
            raise error
        finally:
            session.close()
