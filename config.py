import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = 'APDSDOkowqw019odAD919#@'

SQLALCHEMY_DATABASE_URI = (
    f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
)