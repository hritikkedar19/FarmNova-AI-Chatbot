import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
BASE = Path(__file__).resolve().parent
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret")
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", str(BASE / "uploads"))
    MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "50"))
