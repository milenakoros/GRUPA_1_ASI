import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text

from src.api.main import app
import src.api.main as main_module

client = TestClient(app)

@pytest.fixture
def test_db_engine(tmp_path):
    test_db = tmp_path / "test.db"

    engine = create_engine(
        f"sqlite:///{test_db}",
        future=True,
    )

    with engine.begin() as conn:
        conn.execute(
            text("""
                CREATE TABLE predictions (
                    id INTEGER PRIMARY KEY,
                    ts TEXT,
                    payload TEXT,
                    prediction REAL,
                    model_version TEXT
                )
            """)
        )

    return engine

@pytest.fixture
def dummy_payload():
    dummy_payload = {
        "car_name": 39,
        "yr_mfr": 11,
        "fuel_type": 1,
        "kms_run": 28652,
        "city": 1,
        "times_viewed": 483,
        "body_type": 0,
        "transmission": 0,
        "variant": 171,
        "assured_buy": 1,
        "registered_city": 15,
        "registered_state": 5,
        "is_hot": 1,
        "rto": 43,
        "source": 0,
        "make": 9,
        "model": 6,
        "car_availability": 1,
        "total_owners": 2,
        "broker_quote": 386415,
        "original_price": 395599.0,
        "car_rating": 2,
        "fitness_certificate": 1,
        "emi_starts_from": 9189,
        "booking_down_pymnt": 59340,
        "reserved": 0,
        "warranty_avail": 0
    }

    return dummy_payload

def test_validation_error():
    r = client.post("/predict", json={"feature_num": "oops", "feature_cat": "A"})
    assert r.status_code == 422

def test_predict_and_db_write(test_db_engine, dummy_payload):
    main_module.engine = test_db_engine

    with test_db_engine.connect() as conn:
        before = conn.execute(
            text("SELECT COUNT(*) FROM predictions")
        ).scalar()

    response = client.post("/predict", json=dummy_payload)
    assert response.status_code == 200

    with test_db_engine.connect() as conn:
        after = conn.execute(
            text("SELECT COUNT(*) FROM predictions")
        ).scalar()

    assert after == before + 1

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}
