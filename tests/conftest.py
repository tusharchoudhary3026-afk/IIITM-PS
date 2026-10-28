import sys, pathlib, pytest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))


@pytest.fixture
def db(tmp_path, monkeypatch):
    from core import db as dbm
    monkeypatch.setattr(dbm, "DB_PATH", tmp_path / "test.db")
    dbm.init_db()
    return dbm
