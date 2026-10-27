
import yfinance as yf
from sqlalchemy import text
from database import engine
from logger_config import logger
from datetime import datetime

stocks = {
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "NVDA": "NVIDIA"
}

run_id = None
records_processed = 0
started_at = datetime.now()

try:
    with engine.begin() as connection:
        result = connection.execute(
            text("""
                INSERT INTO pipeline_runs (started_at, status)
                VALUES (:started_at, 'RUNNING')
                RETURNING run_id
            """),
            {"started_at": started_at}
        )
        run_id = result.scalar_one()

    logger.info("Starting stock market data pipeline.")

    for ticker, company_name in stocks.items():
        logger.info("Fetching data for %s", ticker)

        with engine.begin() as connection:
            connection.execute(
                text("""
                    INSERT INTO stocks (ticker, company_name)
                    VALUES (:ticker, :company_name)
                    ON CONFLICT (ticker)
                    DO UPDATE SET company_name = EXCLUDED.company_name
                """),
                {"ticker": ticker, "company_name": company_name}
            )

        data = yf.download(
            ticker,
            period="1mo",
            interval="1d",
            auto_adjust=True,
            progress=False
        )

        if data.empty:
            logger.warning("No data found for %s", ticker)
            continue

        data = data.reset_index()

        if getattr(data.columns, "nlevels", 1) > 1:
            data.columns = data.columns.get_level_values(0)

        with engine.begin() as connection:
            stock_id = connection.execute(
                text("SELECT stock_id FROM stocks WHERE ticker = :ticker"),
                {"ticker": ticker}
            ).scalar_one()

            for _, row in data.iterrows():
                result = connection.execute(
                    text("""
                        INSERT INTO daily_prices
                        (stock_id, trade_date, open_price, high_price,
                         low_price, close_price, volume)
                        VALUES
                        (:stock_id, :trade_date, :open_price, :high_price,
                         :low_price, :close_price, :volume)
                        ON CONFLICT (stock_id, trade_date) DO NOTHING
                    """),
                    {
                        "stock_id": stock_id,
                        "trade_date": row["Date"].date(),
                        "open_price": float(row["Open"]),
                        "high_price": float(row["High"]),
                        "low_price": float(row["Low"]),
                        "close_price": float(row["Close"]),
                        "volume": int(row["Volume"])
                    }
                )

                records_processed += result.rowcount

        logger.info("Finished processing %s", ticker)

    with engine.begin() as connection:
        connection.execute(
            text("""
                UPDATE pipeline_runs
                SET finished_at = :finished_at,
                    status = 'SUCCESS',
                    records_processed = :records_processed
                WHERE run_id = :run_id
            """),
            {
                "finished_at": datetime.now(),
                "records_processed": records_processed,
                "run_id": run_id
            }
        )

    logger.info(
        "Pipeline completed. New records inserted: %s",
        records_processed
    )

except Exception as error:
    logger.exception("Pipeline failed.")

    if run_id is not None:
        with engine.begin() as connection:
            connection.execute(
                text("""
                    UPDATE pipeline_runs
                    SET finished_at = :finished_at,
                        status = 'FAILED',
                        records_processed = :records_processed,
                        error_message = :error_message
                    WHERE run_id = :run_id
                """),
                {
                    "finished_at": datetime.now(),
                    "records_processed": records_processed,
                    "error_message": str(error)[:2000],
                    "run_id": run_id
                }
            )

    raise
