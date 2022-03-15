import os
from pathlib import Path
import json
import pytest

from fastapi.testclient import TestClient

from main import app
from pydantic_schemas import TagIncrementPydantic

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_pydantic_raises_exception_invalid_tag_name():
    _ = TagIncrementPydantic(name="bird", value=4)

    with pytest.raises(Exception):
        _ = TagIncrementPydantic(name="am", value=55)

    with pytest.raises(Exception):
        _ = TagIncrementPydantic(name="a_really_really_long_tag_name_so_long", value=55)


def test_api_tags_increment_and_statistics():
    test_file_path = Path(os.environ['DB_CONN'])

    if test_file_path.exists():
        os.remove(test_file_path)

    pigeon = TagIncrementPydantic(name="pigeon", value=17)
    cats = TagIncrementPydantic(name="cat", value=8)
    pigeon2 = TagIncrementPydantic(name="pigeon", value=9)
    _ = client.post("/tags/increment",  json=pigeon.dict())
    _ = client.post("/tags/increment", json=pigeon2.dict())
    _ = client.post("/tags/increment", json=cats.dict())
    stat = client.get("/tags/statistics")
    resp_dict = json.loads(stat.content)
    assert resp_dict['pigeon'] == 26
    assert resp_dict['cat'] == 8



