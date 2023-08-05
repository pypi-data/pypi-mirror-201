from datetime import datetime

from pydantic import BaseModel


class MemsourceAuthTokenModel(BaseModel):
    token: str
    expires: datetime


class MemsourceResponse(BaseModel):
    totalElements: int
    totalPages: int
    pageSize: int
    pageNumber: int
    numberOfElements: int
    content: list
