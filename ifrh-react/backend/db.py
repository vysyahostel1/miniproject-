import os
import psycopg
from contextlib import contextmanager

DB_URL = os.getenv('NEON_DATABASE_URL', '')

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  first_name TEXT,
  last_name TEXT,
  email TEXT UNIQUE NOT NULL,
  phone TEXT,
  password_hash TEXT NOT NULL,
  status TEXT DEFAULT 'active',
  created_at TIMESTAMP DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS research_requests (
  req_id TEXT PRIMARY KEY,
  name TEXT,
  email TEXT,
  phone TEXT,
  type TEXT,
  priority TEXT,
  subject TEXT,
  message TEXT,
  status TEXT DEFAULT 'new',
  date TEXT,
  timestamp TIMESTAMP DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS reports (
  id SERIAL PRIMARY KEY,
  title TEXT,
  category TEXT,
  date TEXT,
  size TEXT,
  status TEXT,
  url TEXT
);
CREATE TABLE IF NOT EXISTS site_data (
  key TEXT PRIMARY KEY,
  value JSONB,
  updated_at TIMESTAMP DEFAULT NOW()
);
"""

@contextmanager
def get_conn():
  with psycopg.connect(DB_URL, autocommit=True) as conn:
    yield conn

def init_db():
  if not DB_URL:
    return
  with get_conn() as conn:
    with conn.cursor() as cur:
      cur.execute(SCHEMA_SQL)
