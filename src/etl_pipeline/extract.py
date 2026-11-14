"""Extract JSON records from the REST API."""
from typing import Any
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from .config import API_BASE_URL, API_TIMEOUT
from .logger import get_logger

logger = get_logger(__name__)

def create_session() -> requests.Session:
    """Create a session with retries for transient HTTP failures."""
    retry = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset(["GET"]),
    )
    session = requests.Session()
    session.mount("https://", HTTPAdapter(max_retries=retry))
    session.mount("http://", HTTPAdapter(max_retries=retry))
    return session

def fetch_endpoint(endpoint: str, session: requests.Session | None = None) -> list[dict[str, Any]]:
    """Fetch a list of JSON objects from an API endpoint."""
    client = session or create_session()
    url = f"{API_BASE_URL}/{endpoint.lstrip('/')}"
    logger.info("Requesting %s", url)
    response = client.get(url, timeout=API_TIMEOUT)
    response.raise_for_status()
    payload = response.json()

    if not isinstance(payload, list):
        raise ValueError(f"Expected a list response from {url}")

    if not all(isinstance(item, dict) for item in payload):
        raise ValueError(f"Expected every item from {url} to be a JSON object")

    logger.info("Extracted %d records from %s", len(payload), endpoint)
    return payload

def extract_data() -> tuple[list[dict], list[dict]]:
    """Extract users and posts from the source API."""
    with create_session() as session:
        users = fetch_endpoint("users", session)
        posts = fetch_endpoint("posts", session)
    return users, posts
