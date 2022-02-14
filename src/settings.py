import os

APP_ORIGIN = os.environ.get("APP_ORIGIN") # localhost or site

if hostname := os.environ.get("RDS_HOSTNAME"):
    # When running on Beanstalk, it automatically sets all these values for the attached RDS:
    username = os.environ["RDS_USERNAME"]
    password = os.environ["RDS_PASSWORD"]
    db_name = os.environ["RDS_DB_NAME"]
    port = os.environ["RDS_PORT"]
    DATABASE_URL = (
        f"postgresql://{username}:{password}@{hostname}:{port}/{db_name}"
    )
else:
    # For local development
    DATABASE_URL = os.environ["DATABASE_URL"]
