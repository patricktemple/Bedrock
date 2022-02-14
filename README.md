# Bedrock sample app - File Uploader

This is a simple web app which allows users to upload arbitrary JSON files and share a link
to download them. Files are limited to 1 MB in size.

Stack:
- Python/Flask
- Postgres
- Docker running on Elastic Beanstalk

## Setup

You'll need to set up a virtual environment first:
```bash
pyenv install 3.9.5
pyenv virtualenv 3.9.5 bedrock
pip install pip-tools
pip install -r requirements.txt
```

Then you'll need to set a local `.env` file. You can get it started from the template:
```bash
cp env-template.env .env
```

Right now the template is complete, because it does not need to contain any secrets.
If new environment variables are defined that do need to be kept out of Github,
they should be defined in `env-template.env` but with values left blank.

## Running locally

The following will build the Docker file of the Flask app, then run a local server:
```bash
script/run
```

Then just visit `http://localhost` in your browser.

## Formatting
Run `fourmat` to autoformat the Python code.

## Deploy
This runs on Elastic Beanstalk. You'll need to have your environment configured
for the EB app. Then you can run `eb deploy` to push it to prod (which is currently the only
environment).
