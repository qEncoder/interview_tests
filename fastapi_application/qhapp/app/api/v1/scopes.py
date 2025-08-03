import logging

from fastapi import APIRouter, status, Depends

from qhapp.app.schemas.scopes import ScopeCreate, ScopeRead
from qhapp.app.crud.scopes import crud_scope
from qhapp.app.database.db import get_db_session_async, AsyncSession

router = APIRouter(prefix="/scopes", tags=["Scopes"])

logger = logging.getLogger(__name__)

@router.post("",status_code=status.HTTP_201_CREATED,
                response_model=ScopeRead,
                summary="Create a new scope",)
async def create_scope(scopeCreate: ScopeCreate, 
                        session: AsyncSession = Depends(get_db_session_async)):
    """
    Create a new scope with the given information.
    
    Returns:
        ScopeRead: The created scope.
    """
    scope = await crud_scope.create(session, scopeCreate)
    print(scope, scope.uuid, scope.name)
    return ScopeRead.model_validate(scope)