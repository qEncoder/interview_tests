from __future__ import annotations

import logging
import os
from typing import AsyncGenerator, Callable

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)


class Database:
    """Lazy-initialised, thread-safe singleton around SQLAlchemy async engine."""

    _instance: Database | None = None
    _engine: AsyncEngine
    _session_factory: Callable[[], AsyncSession]

    def __new__(cls, database_url: str | None = None) -> "Database":  # type: ignore[override]
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            db_url = database_url or os.getenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:")

            logger.info("Creating async SQLAlchemy engine for %s", db_url)
            cls._engine = create_async_engine(
                db_url,
                echo=os.getenv("SQLALCHEMY_ECHO", "false").lower() == "true",
                future=True,
                connect_args={"check_same_thread": False} if db_url.startswith("sqlite") else {},
            )

            cls._session_factory = sessionmaker(
                bind=cls._engine,
                class_=AsyncSession,
                autoflush=False,
                expire_on_commit=False,
            )
        return cls._instance

    @property
    def engine(self) -> AsyncEngine:
        """Return the underlying SQLAlchemy :class:`AsyncEngine`."""

        return self._engine

    @property
    def session_factory(self) -> Callable[[], AsyncSession]:
        """Return a *factory* that creates new AsyncSession instances."""

        return self._session_factory

    async def dispose(self) -> None:
        """Dispose of the engine's connection pool.

        This can be useful in teardown logic for test suites.
        """

        await self._engine.dispose()

db = Database()

async def init_db() -> None:
    """Create all tables for the current metadata on the configured engine."""

    # Import lazily to avoid circular dependencies
    from qhapp.app.models.base import Base

    async with db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db_session_async() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields a single database session.

    The session is committed on successful exit or rolled back when an
    exception bubbles up.
    """

    async with db.session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:  # noqa: BLE001  (catch-all rollback is intentional)
            await session.rollback()
            raise
