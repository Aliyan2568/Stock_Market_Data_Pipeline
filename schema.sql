
CREATE TABLE stocks (
    stock_id SERIAL PRIMARY KEY,
    ticker VARCHAR(10) UNIQUE NOT NULL,
    company_name VARCHAR(100)
);

CREATE TABLE daily_prices (
    price_id BIGSERIAL PRIMARY KEY,
    stock_id INTEGER REFERENCES stocks(stock_id),
    trade_date DATE NOT NULL,
    open_price NUMERIC(12, 4),
    high_price NUMERIC(12, 4),
    low_price NUMERIC(12, 4),
    close_price NUMERIC(12, 4),
    volume BIGINT,
    UNIQUE (stock_id, trade_date)
);

CREATE TABLE pipeline_runs (
    run_id BIGSERIAL PRIMARY KEY,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    finished_at TIMESTAMP,
    status VARCHAR(20),
    records_processed INTEGER DEFAULT 0,
    error_message TEXT
);
