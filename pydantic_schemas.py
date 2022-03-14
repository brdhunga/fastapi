from pydantic import BaseModel, validator


TagName = str


class TagIncrementPydantic(BaseModel):
    name: str
    value: int

    @validator('name')
    def validate_name_length(cls, tag_name: str) -> TagName:
        """"""
        if not (len(tag_name) >= 3 and len(tag_name) <= 15):
            raise Exception("Tag name should be between length of 3 and 15")
        return tag_name
