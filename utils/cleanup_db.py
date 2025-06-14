import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Fetch path
DB_FILE = os.getenv("TEST_SQLITE_DB_PATH")

def cleanup_db():
    if not DB_FILE:
        print("❌ Environment variable TEST_SQLITE_DB_PATH is not set.")
        return

    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print(f"🧹 Deleted {DB_FILE}.")
    else:
        print(f"ℹ️ No DB file found at {DB_FILE} to delete.")

if __name__ == "__main__":
    cleanup_db()
