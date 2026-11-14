"""Run the complete API-to-MySQL ETL workflow."""
from .database import create_tables, get_engine
from .extract import extract_data
from .load import load_posts, load_users
from .logger import get_logger
from .transform import transform_posts, transform_users

logger = get_logger(__name__)

def run_pipeline() -> dict[str, int]:
    """Execute extraction, transformation, and loading in dependency order."""
    logger.info("ETL pipeline started")
    engine = get_engine()
    try:
        raw_users, raw_posts = extract_data()
        users_df = transform_users(raw_users)
        valid_user_ids = set(users_df["id"].tolist())
        posts_df = transform_posts(raw_posts, valid_user_ids)

        create_tables(engine)
        users_loaded = load_users(engine, users_df)
        posts_loaded = load_posts(engine, posts_df)

        summary = {
            "users_extracted": len(raw_users),
            "posts_extracted": len(raw_posts),
            "users_loaded": users_loaded,
            "posts_loaded": posts_loaded,
        }
        logger.info("ETL pipeline completed successfully: %s", summary)
        return summary
    except Exception:
        logger.exception("ETL pipeline failed")
        raise
    finally:
        engine.dispose()

if __name__ == "__main__":
    run_pipeline()
