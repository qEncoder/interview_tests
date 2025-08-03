from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from qhapp.app.schemas.scopes import ScopeCreate
from qhapp.app.models.scopes import Scopes
from qhapp.app.exceptions.scopes import ScopeUUIDInUse

class CRUDScope:
    async def create(self, session: AsyncSession, scope_create: ScopeCreate) -> Scopes:
        """
        Create a new scope.

        Args:
            session (AsyncSession): The database session.
            scope_create (ScopeCreate): The scope creation data.

        Returns:
            Scopes: The created scope.
        """
        stmt = select(Scopes).filter(Scopes.uuid == scope_create.uuid)
        result = await session.execute(stmt)
        if result.scalar_one_or_none():
            raise ScopeUUIDInUse(scope_create.uuid)
        
        scope = Scopes(**scope_create.model_dump())
        session.add(scope)
        await session.commit()
        await session.refresh(scope)
        return scope
    
crud_scope = CRUDScope()