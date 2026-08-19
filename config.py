import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

def load_env_file():
    """Manual parser for .env to eliminate external dependency requirements."""
    if not ENV_FILE.exists():
        return
    try:
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip().strip("'").strip('"')
                    if key not in os.environ:
                        os.environ[key] = val
    except Exception as e:
        print(f"⚠️ [CONFIG WARNING] Gagal memuat .env: {e}")

load_env_file()

# LinkedIn OAuth Credentials
LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID", "")
LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET", "")
LINKEDIN_REDIRECT_URI = os.getenv("LINKEDIN_REDIRECT_URI", "http://localhost:8000/callback")
LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN", "")
LINKEDIN_PERSON_URN = os.getenv("LINKEDIN_PERSON_URN", "") # Format: urn:li:person:XXXXX

# Execution Settings
MOCK_MODE = os.getenv("MOCK_MODE", "True").lower() in ("true", "1", "yes")
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "id").lower() # 'id' atau 'en'
POST_DELAY_SECONDS = int(os.getenv("POST_DELAY_SECONDS", "3"))

# Validation Check
def is_live_ready() -> bool:
    return bool(LINKEDIN_ACCESS_TOKEN and LINKEDIN_PERSON_URN and not MOCK_MODE)
