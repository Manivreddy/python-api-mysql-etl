"""Load transformed DataFrames into MySQL using idempotent upserts."""
import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine
from .logger import get_logger

logger = get_logger(__name__)

USER_UPSERT = text("""
INSERT INTO users (id, name, username, email, phone, website)
VALUES (:id, :name, :username, :email, :phone, :website)
ON DUPLICATE KEY UPDATE
    name = VALUES(name),
    username = VALUES(username),
    email = VALUES(email),
    phone = VALUES(phone),
    website = VALUES(website)
""")

POST_UPSERT = text("""
INSERT INTO posts (id, user_id, title, body)
VALUES (:id, :user_id, :title, :body)
ON DUPLICATE KEY UPDATE
    user_id = VALUES(user_id),
    title = VALUES(title),
    body = VALUES(body)
""")

def load_users(engine: Engine, df: pd.DataFrame) -> int:
    """Insert or update users and return the number of processed rows."""
    if df.empty:
        logger.warning("No user records to load")
        return 0
    records = df.where(pd.notna(df), None).to_dict(orient="records")
    with engine.begin() as connection:
        connection.execute(USER_UPSERT, records)
    logger.info("Loaded %d user records", len(records))
    return len(records)

def load_posts(engine: Engine, df: pd.DataFrame) -> int:
    """Insert or update posts and return the number of processed rows."""
    if df.empty:
        logger.warning("No post records to load")
        return 0
    records = df.where(pd.notna(df), None).to_dict(orient="records")
    with engine.begin() as connection:
        connection.execute(POST_UPSERT, records)
    logger.info("Loaded %d post records", len(records))
    return len(records)
