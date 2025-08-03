from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from qhapp.app.models.base import Base

class Scopes(Base):
    __tablename__ = "scopes"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[UUID] = mapped_column(unique=True)
    name : Mapped[str]