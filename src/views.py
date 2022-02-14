from .app import app

from .models import DataFile


@app.route("/healthz", methods=["GET"])
def healthz():
    return "Healthy!"


@app.route("/", methods=["GET"])
def home():
    return "Hello world!"


@app.route("/file/<uuid:file_id>", methods=["GET"])
def get_file(file_id):
    data_file = DataFile.query.get(file_id)
    # TODO: Check token and 403? Or get rid of token
    # TODO: content type
    return data_file.json_body