from fastapi.routing import APIRouter

from qhapp.app.api.v1 import scopes

v1_router = APIRouter(prefix='/api/v1')
v1_router.include_router(scopes.router)