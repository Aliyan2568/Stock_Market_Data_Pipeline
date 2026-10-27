from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Stock Market Data API is running"


def test_get_stocks():
    response = client.get("/stocks")

    assert response.status_code == 200

    tickers = [stock["ticker"] for stock in response.json()]

    assert "AAPL" in tickers
    assert "MSFT" in tickers
    assert "NVDA" in tickers


def test_get_stock_prices():
    response = client.get("/stocks/AAPL")

    assert response.status_code == 200

    prices = response.json()

    assert len(prices) > 0
    assert prices[0]["ticker"] == "AAPL"
    assert "close_price" in prices[0]
    assert "volume" in prices[0]


def test_unknown_stock():
    response = client.get("/stocks/NOTASTOCK")

    assert response.status_code == 404


def test_invalid_limit():
    response = client.get("/stocks/AAPL?limit=500")

    assert response.status_code == 400
