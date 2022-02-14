import pytest

from src.app import app
from src.models import DataFile, db
from uuid import uuid4

import json

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_file(client):
    file_id = uuid4()
    test_file = DataFile(id=file_id, json_body='{"key": 3}', secret_token="token")
    db.session.add(test_file)
    db.session.commit()

    response = client.get(f"/file/{file_id}?token=token")

    assert json.loads(response.data) == {"key": 3}


def test_get_file__bad_token(client):
    file_id = uuid4()
    test_file = DataFile(id=file_id, json_body='{"key": 3}', secret_token="token")
    db.session.add(test_file)
    db.session.commit()

    response = client.get(f"/file/{file_id}?token=wrong")

    assert response.status_code == 403