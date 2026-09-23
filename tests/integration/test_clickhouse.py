import pytest

pytestmark = pytest.mark.integration


def _clickhouse_up() -> bool:
    try:
        import clickhouse_connect

        client = clickhouse_connect.get_client(host="localhost", port=8123)
        client.command("SELECT 1")
        return True
    except Exception:
        return False


@pytest.mark.skipif(not _clickhouse_up(), reason="ClickHouse not reachable")
def test_clickhouse_reachable():
    assert _clickhouse_up()