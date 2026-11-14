import pytest
from etl_pipeline.extract import fetch_endpoint

class FakeResponse:
    def __init__(self, payload):
        self.payload = payload
    def raise_for_status(self):
        pass
    def json(self):
        return self.payload

class FakeSession:
    def __init__(self, payload):
        self.payload = payload
        self.last_url = None
        self.last_timeout = None
    def get(self, url, timeout):
        self.last_url = url
        self.last_timeout = timeout
        return FakeResponse(self.payload)

def test_fetch_endpoint_returns_json_records():
    session = FakeSession([{"id": 1, "name": "Test"}])
    result = fetch_endpoint("users", session=session)
    assert result == [{"id": 1, "name": "Test"}]
    assert session.last_url.endswith("/users")
    assert session.last_timeout > 0

def test_fetch_endpoint_rejects_non_list_payload():
    with pytest.raises(ValueError):
        fetch_endpoint("users", session=FakeSession({"id": 1}))

def test_fetch_endpoint_rejects_non_object_items():
    with pytest.raises(ValueError):
        fetch_endpoint("users", session=FakeSession(["not-an-object"]))
