from fastapi import FastAPI

from qhapp.app.api import v1_router
from qhapp.lifespan import lifespan

app = FastAPI(lifespan=lifespan)
app.include_router(router=v1_router)