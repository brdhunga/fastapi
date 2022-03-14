import pytest
from fastapi.testclient import  TestClient

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



