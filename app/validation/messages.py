from pydantic import BaseModel, field_validator
from typing import Optional


""" Request Validation Classes """

class FilterDatasetRequest(BaseModel):
    """ BaseModel for Searching with a Query. """
    query: str

    @field_validator('query')
    def validate_query(cls, query: str) -> str:
        return query


""" Response Validation Classes """

class MessageResponse(BaseModel):
    """ BaseModel for a default Message Response. """
    msg: str
    code: int
    data: Optional[dict] = None

class DataResponse(BaseModel):
    """ BaseModel for a default Data Response. """
    msg: str
    code: int
    data: dict

    def check_data(self) -> None:
        pass
