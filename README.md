# Python API-to-MySQL ETL Data Pipeline

A modular ETL (Extract, Transform, Load) project that retrieves users and posts from the public [JSONPlaceholder REST API](https://jsonplaceholder.typicode.com/), cleans and validates the records with Python and Pandas, and loads them into relational MySQL tables.

## Project overview

```text
JSONPlaceholder REST API
          |
          v
   Extract (Requests)
          |
          v
 Transform (Pandas)
 - normalize fields
 - clean text
 - validate required values
 - remove duplicates
          |
          v
   Load (SQLAlchemy)
 - create schema
 - upsert users
 - upsert posts
          |
          v
       MySQL
   users | posts
```

### Tech stack

- Python 3.10+
- REST API / JSON
- Requests
- Pandas
- MySQL 8
- SQLAlchemy + PyMySQL
- pytest
- Docker Compose
- Git / GitHub

## Features

- Fetches users and posts from REST API endpoints.
- Uses configurable request timeout and retry behavior.
- Converts API JSON payloads into Pandas DataFrames.
- Cleans whitespace and normalizes records.
- Checks required fields, invalid identifiers, and duplicate IDs.
- Loads data into relational MySQL tables with primary and foreign keys.
- Uses MySQL upsert logic so rerunning the pipeline does not create duplicate rows.
- Logs pipeline progress and failures to both console and `logs/etl_pipeline.log`.
- Separates extraction, transformation, loading, and orchestration into reusable modules.
- Includes automated unit tests and an optional live-MySQL integration test.

## Repository structure

```text
python-api-mysql-etl/
├── src/
│   └── etl_pipeline/
│       ├── __init__.py
│       ├── config.py
│       ├── database.py
│       ├── extract.py
│       ├── transform.py
│       ├── load.py
│       ├── pipeline.py
│       └── logger.py
├── sql/
│   └── schema.sql
├── tests/
│   ├── conftest.py
│   ├── test_extract.py
│   ├── test_transform.py
│   └── test_integration_mysql.py
├── logs/
│   └── .gitkeep
├── .env.example
├── .gitignore
├── docker-compose.yml
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## 1. Prerequisites

Install:

- Python 3.10 or newer
- Git
- Docker Desktop (recommended), or a local MySQL 8 server

## 2. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/python-api-mysql-etl.git
cd python-api-mysql-etl
```

## 3. Create and activate a virtual environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 4. Install dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## 5. Configure MySQL

### Option A: Start MySQL with Docker (recommended)

```bash
docker compose up -d
```

This starts MySQL 8 and creates the `etl_database` database using the credentials in `docker-compose.yml`. Change those development-only credentials before using this setup beyond a local machine.

### Option B: Use an existing MySQL server

Create a database:

```sql
CREATE DATABASE etl_database;
```

Copy the environment template:

**Windows:**
```powershell
Copy-Item .env.example .env
```

**macOS / Linux:**
```bash
cp .env.example .env
```

Edit `.env` with your local MySQL host, port, database, username, and password. Do not commit `.env`.

## 6. Run the ETL pipeline

From the project root, set the source directory on the module path:

**Windows PowerShell:**
```powershell
$env:PYTHONPATH = "src"
python -m etl_pipeline.pipeline
```

**macOS / Linux:**
```bash
PYTHONPATH=src python -m etl_pipeline.pipeline
```

The pipeline will:

1. Fetch users from `/users`.
2. Fetch posts from `/posts`.
3. Clean and validate both datasets.
4. Create the MySQL tables if they do not exist.
5. Insert or update users and posts.
6. Print a run summary and write logs.

## 7. Run tests

```bash
pytest
```

The default test suite uses mocked API responses and does not require a running MySQL instance.

To run the optional live database integration test, set `RUN_MYSQL_INTEGRATION=1` in your environment after configuring MySQL:

**Windows PowerShell:**
```powershell
$env:RUN_MYSQL_INTEGRATION = "1"
pytest tests/test_integration_mysql.py -v
```

**macOS / Linux:**
```bash
RUN_MYSQL_INTEGRATION=1 pytest tests/test_integration_mysql.py -v
```

## Database design

### `users`

| Column | Type | Description |
|---|---|---|
| `id` | INT | API user ID; primary key |
| `name` | VARCHAR(150) | User name |
| `username` | VARCHAR(100) | Username |
| `email` | VARCHAR(150) | Email address |
| `phone` | VARCHAR(100) | Phone |
| `website` | VARCHAR(150) | Website |

### `posts`

| Column | Type | Description |
|---|---|---|
| `id` | INT | API post ID; primary key |
| `user_id` | INT | Author ID; foreign key to `users.id` |
| `title` | VARCHAR(500) | Post title |
| `body` | TEXT | Post content |

## Useful SQL queries

```sql
-- Total users and posts
SELECT COUNT(*) AS total_users FROM users;
SELECT COUNT(*) AS total_posts FROM posts;

-- Posts written by each user
SELECT u.name, COUNT(p.id) AS post_count
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
GROUP BY u.id, u.name
ORDER BY post_count DESC;

-- Preview the latest IDs loaded
SELECT * FROM posts ORDER BY id DESC LIMIT 10;

-- Find users without posts
SELECT u.id, u.name
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
WHERE p.id IS NULL;
```

## Configuration

See `.env.example` for supported settings:

- `API_BASE_URL`: REST API base URL.
- `API_TIMEOUT`: request timeout in seconds.
- `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`: MySQL connection details.
- `LOG_LEVEL`: logging level.

## Notes and limitations

- JSONPlaceholder is a public demo API. Its data is synthetic and intended for learning and testing.
- This project demonstrates a batch ETL workflow, not a production streaming platform.
- Credentials are read from environment variables. Never commit real passwords or API secrets.
- The API's user and post IDs are retained as primary keys; reruns update matching records instead of inserting duplicates.

## Future improvements

- Add scheduling with cron or Apache Airflow.
- Add incremental extraction using API pagination or updated timestamps where supported.
- Add data-quality metrics and a pipeline run-history table.
- Containerize the Python application alongside MySQL.
- Add CI with GitHub Actions.

## Author

**Mani Vighneswar Reddy**

Add your LinkedIn and GitHub profile links here before publishing.
