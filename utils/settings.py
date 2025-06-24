import os

from sqlalchemy import create_engine

DB_USER = os.getenv("DB_USERNAME", "postgres").strip()
DB_PASSWORD = os.getenv("DB_PASSWORD", "timescaledb").strip()
DB_IP = os.getenv("DB_IP", "localhost").strip()
DB_NAME = os.getenv("DB_NAME", "ai").strip()

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_IP}:5432/{DB_NAME}")
os.environ["CONNECTION_URL"] = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_IP}:5432/{DB_NAME}"