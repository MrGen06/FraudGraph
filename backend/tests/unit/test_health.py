from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_liveness_check() -> None:
    response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "alive"}


@patch("app.api.v1.health.check_redis", return_value=True)
@patch("app.api.v1.health.check_neo4j", return_value=True)
@patch("app.api.v1.health.check_postgres", return_value=True)
def test_readiness_check_when_all_dependencies_are_healthy(
    mock_postgres,
    mock_neo4j,
    mock_redis,
) -> None:
    response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ready",
        "checks": {
            "postgres": "ok",
            "neo4j": "ok",
            "redis": "ok",
        },
    }


@patch("app.api.v1.health.check_redis", return_value=True)
@patch("app.api.v1.health.check_neo4j", return_value=False)
@patch("app.api.v1.health.check_postgres", return_value=True)
def test_readiness_check_when_neo4j_is_unavailable(
    mock_postgres,
    mock_neo4j,
    mock_redis,
) -> None:
    response = client.get("/health/ready")

    assert response.status_code == 503
    assert response.json() == {
        "detail": {
            "status": "not_ready",
            "checks": {
                "postgres": "ok",
                "neo4j": "unavailable",
                "redis": "ok",
            },
        }
    }
