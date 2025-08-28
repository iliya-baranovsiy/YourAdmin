import os
from dotenv import load_dotenv

load_dotenv()

DATA_BASE_URL = os.getenv("DATA_BASE_URL")
TOKEN = os.getenv("TOKEN")
ASYNC_DATA_BASE_URL = os.getenv("ASYNC_DATA_BASE_URL")
