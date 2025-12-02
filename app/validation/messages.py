from pydantic import BaseModel, field_validator
from typing import Optional


""" Request Validation Classes """

class FilterDatasetRequest(BaseModel):
    query: str

    @field_validator('query')
    def validate_query(cls, query: str) -> str:
        return query


""" Response Validation Classes """

class MessageResponse(BaseModel):
    msg: str
    code: int
    data: Optional[dict] = None

    def log(self) -> None:
        pass

class DataResponse(BaseModel):
    msg: str
    code: int
    data: dict

    def check_data(self) -> None:
        pass

    def log(self) -> None:
        pass
