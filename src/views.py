import csv
import json
import logging
import secrets

from flask import render_template, request
from werkzeug import exceptions

from .app import app
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
    if data_file.secret_token != request.args.get("token"):
        raise exceptions.Forbidden()
    return app.response_class(
        response=data_file.json_body, mimetype="application/json"
    )


@app.route("/upload", methods=["POST"])
def upload_file():
    data = request.files["json_file"]
    try:
        data_str = data.read().decode("utf-8")
        csv_reader = csv.reader(data_str.split("\n"))
        fields = next(csv_reader)
        if set(fields) != {"timestamp", "lon", "lat", "depth"}:
            return render_template("upload_failure.html"), 400

        fields_by_index = {}
        for index, field in enumerate(fields):
            fields_by_index[index] = field

        data = []
        for row in csv_reader:
            row_json = {}
            for index, value in enumerate(row):
                # TODO: Validate the values
                field_name = fields_by_index[index]
                row_json[field_name] = value
            data.append(row_json)

    except (UnicodeDecodeError):
        logging.exception("JSON decode error on file upload")
        return render_template("upload_failure.html"), 400

    data_file = DataFile(
        json_body=json.dumps(data), secret_token=secrets.token_urlsafe()
    )
    db.session.add(data_file)
    db.session.commit()

    return render_template(
        "upload_success.html",
        file_url=f"{APP_ORIGIN}/file/{data_file.id}?token={data_file.secret_token}",
    )
