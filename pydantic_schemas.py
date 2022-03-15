from datetime import datetime
from typing import Literal, Union

from pydantic import BaseModel, validator, Field

from constants import LogSeverityEnum

TagName = str


class TagIncrementPydantic(BaseModel):
    name: str
    value: int

    @validator('name')
    def validate_name_length(cls, tag_name: str) -> TagName:
        """"""
        if not (3 <= len(tag_name) <= 15):
            raise Exception("Tag name should be between length of 3 and 15")
        return tag_name


TagStatisticsDict = dict[str, int]


class LogPydantic(BaseModel):
    log_name: str = Field(..., alias="logName")  # e.g. billingAccounts/[BILLING_ACCOUNT_ID]/logs/[LOG_ID]
    resource: dict[Literal["type"] | Literal["labels"], Union[str | dict]]  # e.g. {"type": "personalLaptop", labels: {
    # "laptopHost": "brdLaptop"}}
    timestamp: datetime
    severity: int  # Literal[0, 100, 200, 300, 400, 500, 600, 700, 800]
    textPayload: str

    @validator('severity')
    def validate_severity_level(cls, v: int) -> int:
        valid_severity_choices = [choice.value for choice in LogSeverityEnum]
        if v not in valid_severity_choices:
            raise Exception(f"severity value can be only of {valid_severity_choices}")
        return v

