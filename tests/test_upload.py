import io
import json
from uuid import uuid4

import pytest

from src.app import app
from src.models import DataFile, db


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def autouse_fixtures():
    db.drop_all()
    db.create_all()

    yield

    db.session.close()


def test_upload_file(client):
    data = {
        "json_file": (
            io.BytesIO(b"timestamp,lat,lon,depth\n2022-02-14T17:00:00,1,2,3"),
            "test.json",
        )
    }
    response = client.post(
        "/upload", data=data, content_type="multipart/form-data"
    )

    assert response.status_code == 200

    data = DataFile.query.one()
    assert json.loads(data.json_body) == [
        {
            "timestamp": "2022-02-14T17:00:00",
            "lat": "1",
            "lon": "2",
            "depth": "3",
        }
    ]


def test_get_file(client):
    file_id = uuid4()
    test_file = DataFile(
        id=file_id, json_body='{"key": 3}', secret_token="token"
    )
    db.session.add(test_file)
    db.session.commit()

    response = client.get(f"/file/{file_id}?token=token")

    assert json.loads(response.data) == {"key": 3}


def test_get_file__bad_token(client):
    file_id = uuid4()
    test_file = DataFile(
        id=file_id, json_body='{"key": 3}', secret_token="token"
    )
    db.session.add(test_file)
    db.session.commit()

    response = client.get(f"/file/{file_id}?token=wrong")

    assert response.status_code == 403
