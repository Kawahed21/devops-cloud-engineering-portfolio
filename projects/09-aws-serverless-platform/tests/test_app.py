import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lambda"))
import app


class FakeTable:
    def __init__(self):
        self.items = []

    def put_item(self, Item):
        self.items.append(Item)


def test_get_health(monkeypatch):
    response = app.handler({"httpMethod": "GET"}, None)
    assert response["statusCode"] == 200
    assert json.loads(response["body"])["status"] == "ok"


def test_post_persists_valid_message(monkeypatch):
    table = FakeTable()
    monkeypatch.setattr(app, "_table", lambda: table)
    response = app.handler({"httpMethod": "POST", "body": '{"message":"hello"}'}, None)
    assert response["statusCode"] == 201
    assert table.items[0]["message"] == "hello"
    assert table.items[0]["id"]


def test_post_rejects_invalid_json():
    response = app.handler({"httpMethod": "POST", "body": "{"}, None)
    assert response["statusCode"] == 400


def test_post_rejects_empty_message():
    response = app.handler({"httpMethod": "POST", "body": '{"message":"  "}'}, None)
    assert response["statusCode"] == 400


def test_rejects_unsupported_method():
    response = app.handler({"httpMethod": "DELETE"}, None)
    assert response["statusCode"] == 405
