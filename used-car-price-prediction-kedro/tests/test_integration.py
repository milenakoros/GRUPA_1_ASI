import sqlite3
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_predict_and_db_write(tmp_path):
    test_db = tmp_path / "test.db"
    from sqlalchemy import create_engine, text

    engine = create_engine(f"sqlite:///{test_db}", future=True)

    # utwórz tabelę
    with engine.begin() as conn:
        conn.execute(
            text("CREATE TABLE IF NOT EXISTS predictions (id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, payload TEXT, prediction REAL, model_version TEXT)")
        )

    before = list(engine.execute(text("SELECT COUNT(*) FROM predictions")))[0][0]

    payload = {"feature_num": 2.9, "feature_cat": "B"}
    response = client.post("/predict", json=payload)
    assert response.status_code == 200

    after = list(engine.execute(text("SELECT COUNT(*) FROM predictions")))[0][0]
    assert after == before + 1
