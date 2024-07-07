import contextlib
from config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB
from sqlalchemy.engine import Engine, create_engine
from sqlalchemy import text
from typing import ContextManager
from collections.abc import Generator
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

SYNC_DB_API = "psycopg2"
ASYNC_DB_API = "asyncpg"

_SYNC_ENGINE: Engine | None = None

def build_connection_string(
    db_api: str = ASYNC_DB_API,
    user: str = POSTGRES_USER,
    password: str = POSTGRES_PASSWORD,
    host: str = POSTGRES_HOST,
    port: str = POSTGRES_PORT,
    db: str = POSTGRES_DB,
) -> str:
    return f"postgresql+{db_api}://{user}:{password}@{host}:{port}/{db}"


def get_sqlalchemy_engine() -> Engine:
    global _SYNC_ENGINE
    if _SYNC_ENGINE is None:
        connection_string = build_connection_string(db_api=SYNC_DB_API)
        _SYNC_ENGINE = create_engine(connection_string, pool_size=40, max_overflow=10)
    return _SYNC_ENGINE

async def warm_up_connections(
    sync_connections_to_warm_up: int = 10
) -> None:
    print("Initializing connection into engine....")
    sync_postgres_engine = get_sqlalchemy_engine()
    print("Connected to the database!")
    connections = [
        sync_postgres_engine.connect() for _ in range(sync_connections_to_warm_up)
    ]
    for conn in connections:
        print("Warming up the connection pool...")
        conn.execute(text("SELECT 1"))
    for conn in connections:
        conn.close()

def get_session_context_manager() -> ContextManager[Session]:
    return contextlib.contextmanager(get_session)()


def get_session() -> Generator[Session, None, None]:
    # The line below was added to monitor the latency caused by Postgres connections
    # during API calls.
    # with tracer.trace("db.get_session"):
    with Session(get_sqlalchemy_engine(), expire_on_commit=False) as session:
        yield session