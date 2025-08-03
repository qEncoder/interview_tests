from fastapi import HTTPException

class ScopeUUIDInUse(HTTPException):
    def __init__(self, uuid: str):
        super().__init__(status_code=400, detail=f"Scope with UUID {uuid} is already in use.")
