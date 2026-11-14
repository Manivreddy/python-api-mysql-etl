"""MySQL engine and schema initialization."""
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from .config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
from .logger import get_logger

logger = get_logger(__name__)

def get_engine() -> Engine:
    """Build a SQLAlchemy engine for MySQL."""
    connection_url = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
    )
    return create_engine(connection_url, pool_pre_ping=True, future=True)

def create_tables(engine: Engine) -> None:
    """Create relational tables when they do not already exist."""
    statements = [
        """
        CREATE TABLE IF NOT EXISTS users (
            id INT PRIMARY KEY,
            name VARCHAR(150) NOT NULL,
            username VARCHAR(100),
            email VARCHAR(150),
            phone VARCHAR(100),
            website VARCHAR(150)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS posts (
            id INT PRIMARY KEY,
            user_id INT NOT NULL,
            title VARCHAR(500) NOT NULL,
            body TEXT,
            CONSTRAINT fk_posts_users
                FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """,
    ]
    with engine.begin() as connection:
        for statement in statements:
            connection.execute(text(statement))
    logger.info("Database tables are ready")
