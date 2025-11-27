import os
from databases import Database
from dotenv import load_dotenv
# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

load_dotenv()
# Default local DB URL if env var not provided
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is required in .env")

# Create database instance
db = Database(DATABASE_URL)

# -------------------------------------------------------------------
# SQL Schema
# -------------------------------------------------------------------

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS games (
    id          TEXT PRIMARY KEY,
    board       JSONB NOT NULL,
    player      TEXT,
    winner      TEXT,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);
"""
async def init_db():
    await db.connect()
    await db.execute(CREATE_TABLE_SQL)
