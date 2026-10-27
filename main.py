
from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from database import engine

app = FastAPI(title="Stock Market Data API")


@app.get("/")
def home():
    return {"message": "Stock Market Data API is running"}


@app.get("/stocks")
def get_stocks():
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT ticker, company_name FROM stocks ORDER BY ticker")
        )

        return [
            {"ticker": row.ticker, "company_name": row.company_name}
            for row in result
        ]


@app.get("/stocks/{ticker}")
def get_stock_prices(ticker: str, limit: int = 30):
    if limit < 1 or limit > 365:
        raise HTTPException(
            status_code=400,
            detail="Limit must be between 1 and 365"
        )

    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT s.ticker, d.trade_date, d.open_price,
                       d.high_price, d.low_price, d.close_price, d.volume
                FROM daily_prices d
                JOIN stocks s ON s.stock_id = d.stock_id
                WHERE s.ticker = :ticker
                ORDER BY d.trade_date DESC
                LIMIT :limit
            """),
            {"ticker": ticker.upper(), "limit": limit}
        )

        rows = result.mappings().all()

    if not rows:
        raise HTTPException(
            status_code=404,
            detail="Stock not found or no price data available"
        )

    return [dict(row) for row in rows]
