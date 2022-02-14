import werkzeug
from .app import app

from werkzeug import exceptions

from flask import render_template, request
import secrets

from .models import DataFile, db

from .settings import APP_ORIGIN


@app.route("/healthz", methods=["GET"])
def healthz():
    return "Healthy!"


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/file/<uuid:file_id>", methods=["GET"])
def get_file(file_id):
    data_file = DataFile.query.get(file_id)
    if data_file.secret_token != request.args.get('secret_token'):
        raise exceptions.Forbidden()
    # TODO: content type
    return data_file.json_body


@app.route("/upload", methods=["POST"])
def upload_file():
    data = request.files['json_file']
    data_str = data.read().decode('utf-8')
    # TODO: Validate it

    data_file = DataFile(json_body=data_str, secret_token=secrets.token_urlsafe())
    db.session.add(data_file)
    db.session.commit()

    file_id = data_file.id

    return render_template("upload_success.html", file_url=f"{APP_ORIGIN}/file/{file_id}?token={data_file.secret_token}")
