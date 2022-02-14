import werkzeug
from .app import app

from werkzeug import exceptions

import logging

from flask import render_template, request
import secrets
import json

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
    if data_file.secret_token != request.args.get('token'):
        raise exceptions.Forbidden()
    return app.response_class(
        response=data_file.json_body,
        mimetype='application/json'
    )


@app.route("/upload", methods=["POST"])
def upload_file():
    data = request.files['json_file']
    try:
        # TODO: Validate that the field structure matches expectations
        data_str = data.read().decode('utf-8')
        json.loads(data_str)
    except json.JSONDecodeError:
        logging.exception("JSON decode error on file upload")
        return render_template("upload_failure.html"), 400

    data_file = DataFile(json_body=data_str, secret_token=secrets.token_urlsafe())
    db.session.add(data_file)
    db.session.commit()

    return render_template("upload_success.html", file_url=f"{APP_ORIGIN}/file/{data_file.id}?token={data_file.secret_token}")
