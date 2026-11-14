"""Clean, normalize, and validate extracted API records."""
import pandas as pd
from .logger import get_logger

logger = get_logger(__name__)

USER_COLUMNS = ["id", "name", "username", "email", "phone", "website"]
POST_COLUMNS = ["id", "user_id", "title", "body"]

def _clean_text(series: pd.Series) -> pd.Series:
    return series.fillna("").astype(str).str.strip()

def transform_users(records: list[dict]) -> pd.DataFrame:
    """Return a cleaned users DataFrame with unique positive IDs."""
    df = pd.DataFrame(records)
    if df.empty:
        return pd.DataFrame(columns=USER_COLUMNS)

    for column in USER_COLUMNS:
        if column not in df.columns:
            df[column] = None

    df = df[USER_COLUMNS].copy()
    df["id"] = pd.to_numeric(df["id"], errors="coerce")
    df = df.dropna(subset=["id"])
    df["id"] = df["id"].astype(int)
    df = df[df["id"] > 0]

    for column in ["name", "username", "email", "phone", "website"]:
        df[column] = _clean_text(df[column])

    df = df.drop_duplicates(subset=["id"], keep="last")
    logger.info("Transformed %d user records", len(df))
    return df.reset_index(drop=True)

def transform_posts(records: list[dict], valid_user_ids: set[int] | None = None) -> pd.DataFrame:
    """Return cleaned posts, excluding invalid IDs and orphaned user references."""
    df = pd.DataFrame(records)
    if df.empty:
        return pd.DataFrame(columns=POST_COLUMNS)

    # JSONPlaceholder names the relationship field "userId"; normalize it.
    if "user_id" not in df.columns and "userId" in df.columns:
        df["user_id"] = df["userId"]
    for column in POST_COLUMNS:
        if column not in df.columns:
            df[column] = None

    df = df[POST_COLUMNS].copy()
    for column in ["id", "user_id"]:
        df[column] = pd.to_numeric(df[column], errors="coerce")
    df = df.dropna(subset=["id", "user_id"])
    df["id"] = df["id"].astype(int)
    df["user_id"] = df["user_id"].astype(int)
    df = df[(df["id"] > 0) & (df["user_id"] > 0)]

    df["title"] = _clean_text(df["title"])
    df["body"] = _clean_text(df["body"])
    df = df[df["title"] != ""]

    if valid_user_ids is not None:
        df = df[df["user_id"].isin(valid_user_ids)]

    df = df.drop_duplicates(subset=["id"], keep="last")
    logger.info("Transformed %d post records", len(df))
    return df.reset_index(drop=True)
