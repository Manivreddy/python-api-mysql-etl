"""Optional live MySQL test. Enable with RUN_MYSQL_INTEGRATION=1."""
import os
import pytest
from sqlalchemy import text
from etl_pipeline.database import create_tables, get_engine
from etl_pipeline.load import load_users, load_posts
from etl_pipeline.transform import transform_users, transform_posts

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_MYSQL_INTEGRATION") != "1",
    reason="Set RUN_MYSQL_INTEGRATION=1 to run live MySQL integration test",
)

def test_mysql_insert_and_relationship():
    engine = get_engine()
    try:
        create_tables(engine)
        users = transform_users([{
            "id": 987654, "name": "Integration Test", "username": "etl_test",
            "email": "etl_test@example.com", "phone": "", "website": ""
        }])
        posts = transform_posts([{
            "id": 987654, "user_id": 987654,
            "title": "Integration post", "body": "Test body"
        }], valid_user_ids={987654})

        assert load_users(engine, users) == 1
        assert load_posts(engine, posts) == 1

        with engine.connect() as connection:
            row = connection.execute(
                text("SELECT title FROM posts WHERE id = 987654")
            ).scalar_one()
            assert row == "Integration post"
            connection.execute(text("DELETE FROM posts WHERE id = 987654"))
            connection.execute(text("DELETE FROM users WHERE id = 987654"))
    finally:
        engine.dispose()
