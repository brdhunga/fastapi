import logging
from collections import defaultdict
from datetime import datetime
from typing import Optional, List

from fastapi import FastAPI
from pydantic import parse_obj_as
from tinydb import TinyDB

from constants import LogSeverityEnum
from logging_service import log_data
from pydantic_schemas import TagIncrementPydantic, TagStatisticsDict, LogPydantic
from db import db_service


app = FastAPI()

logging.basicConfig(level=logging.INFO)
logging.debug(f'Starting........')

@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.post("/tags/increment", response_model=bool, tags=["redactor"])
def increment_tags(tags_for_increment: TagIncrementPydantic):
    """
    End point to update the value of a tag
    :param tags_for_increment: Provide tag in the format {"name" : <tag_name_string>, "value" : <tag_value_int>}
    :return: bool if the post is success else raises standard error
    """
    db_conn = db_service.get_connection()
    table = TinyDB(db_conn).table(db_service.TABLE_NAME)
    log_object = LogPydantic(logName="fastApiInterview/12345/logs/1",
                             resource={"type": "personalLaptop"},
                             timestamp=datetime.now(),
                             severity=LogSeverityEnum.INFO.value,
                             textPayload=tags_for_increment.json(by_alias=True))
    log_data(log_object)
    table.insert(tags_for_increment.dict())
    return True


@app.get("/tags/statistics", response_model=TagStatisticsDict, tags=["redactor"])
def increment_tags():
    """
    Get aggregated counts of all the tags
    :return: get counts of name of each tag and corresponding count e.g {"chair": 400}
    """
    db_name = db_service.get_connection()
    table = TinyDB(db_name).table(db_service.TABLE_NAME)
    documents = table.all()
    list_of_tag_increments = parse_obj_as(List[TagIncrementPydantic], documents)

    tag_counts = defaultdict(lambda : 0)
    for tag_count in list_of_tag_increments:
        tag_counts[tag_count.name] += tag_count.value

    return tag_counts

