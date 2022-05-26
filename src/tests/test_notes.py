import json

import pytest
from starlette import status

from app.api import crud


def test_create_post(test_app, monkeypatch):
    test_request_payload = {"title": "something", "description": "something else"}
    tets_response_payload = {"id": 1, "title": "something", "description": "something else"}

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud, "post", mock_post)

    response = test_app.post("/notes/", data=json.dumps(test_request_payload), )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == tets_response_payload


def test_create_note_invalid_json(test_app):
    response = test_app.post("/notes/", data=json.dumps({"title": "bla-something-bla"}))
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_read_note(test_app, monkeypatch):
    test_data = {"id": 1, "title": "some title", "description": "some description"}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)
    response = test_app.get("/notes/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == test_data


def test_read_note_incorrenct_id(test_app, monkeypatch):
    async def mock_get(id):
        return

    monkeypatch.setattr(crud, "get", mock_get)
    response = test_app.get("/notes/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Note not found"


def test_read_all_notes(test_app, monkeypatch):
    test_data = [
        {"id": 1, "title_1": "something_1", "description": "something else_1"},
        {"id": 2, "title_2": "something_2", "description": "something else_2"}
    ]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(crud, "get_all", mock_get_all)
