from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from qhapp.app.database.db import init_db, db

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Run application-wide startup/shutdown tasks.

    1. On startup: create all tables in the in-memory database.
    2. On shutdown: dispose the SQLAlchemy engine (helpful for tests).
    """

    await init_db()

    yield

    await db.dispose()
