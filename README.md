### Stock Market Data Pipeline

A Python built data pipeline that retrieves historical stock market data, stores it in PostgreSQL, and exposes it through a REST API built with FastAPI.

### Features

- Fetches historical daily stock prices using yfinance
- Stores stock information and daily prices in PostgreSQL
- Prevents duplicate price records using database constraints
- Provides REST API endpoints for retrieving stock data
- Tracks pipeline executions, processed records, and failures
- Logs pipeline activity and errors
- Includes automated tests using pytest

### Tech Stack

- Language: Python
- Data Source: yfinance
- Database: PostgreSQL
- Database Toolkit: SQLAlchemy
- API: FastAPI
- Server: Uvicorn
- Testing: pytest, HTTPX

### Project Structure

stock-market-data-pipeline/
    database.py
    fetch_stocks.py
    logger_config.py
    main.py
    requirements.txt
    .gitignore
    stockmarketpipeline_tests/
         test_main.py

### Setup

# 1. Clone the repository

git clone https://github.com/Aliyan2568/stock-market-data-pipeline.git
cd stock-market-data-pipeline


# 2. Create a virtual environment

python -m venv .venv

.\.venv\Scripts\Activate.ps1

# 3. Install dependencies

python -m pip install -r requirements.txt

# 4. Configure environment variables

Create a `.env` file in the project root:

DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=stock_market_db

Replace the example password with your PostgreSQL password. Do not commit `.env` to GitHub.

# 5. Set up the database

Create a PostgreSQL database named `stock_market_db`.

Open the database and execute the SQL statements in 'schema.sql' to create the required tables.

# 6. Run the data pipeline

python fetch_stocks.py

The pipeline retrieves recent daily prices for AAPL, MSFT, and NVDA and saves new records to PostgreSQL.

# 7. Start the API

python -m uvicorn main:app --reload

Open `http://127.0.0.1:8000/docs` to explore and test the API.

# API Endpoints

| Method |      Endpoint      |               Description               |
|--------|--------------------|-----------------------------------------|
| GET    | `/`                | Check API status                        |
| GET    | `/stocks`          | Retrieve available stocks               |
| GET    | `/stocks/{ticker}` | Retrieve historical prices for a ticker |

Example: `GET /stocks/AAPL?limit=5` returns up to five recent daily price records for Apple.

### Running Tests

python -m pytest -v

The tests cover API responses, stored stock data, unknown tickers, and invalid query parameters.
