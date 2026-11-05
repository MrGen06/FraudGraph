import psycopg
import redis
from fastapi import APIRouter, HTTPException, status
from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError
from psycopg import Error as PostgresError
from redis.exceptions import RedisError

from app.core.config import get_settings

router = APIRouter(tags=["Health"])


def check_postgres(database_url: str) -> bool:
    try:
        url = database_url.replace(
            "postgresql+psycopg://",
            "postgresql://",
            1,
        )
        with psycopg.connect(url, connect_timeout=3):
            return True
    except PostgresError:
        return False


def check_neo4j(uri: str, user: str, password: str) -> bool:
    try:
        driver = GraphDatabase.driver(
            uri,
            auth=(user, password),
            connection_timeout=3,
        )
        try:
            driver.verify_connectivity()
            return True
        finally:
            driver.close()
    except (Neo4jError, OSError):
        return False


def check_redis(redis_url: str) -> bool:
    try:
        client = redis.Redis.from_url(
            redis_url,
            socket_connect_timeout=3,
            socket_timeout=3,
        )
        try:
            return bool(client.ping())
        finally:
            client.close()
    except (RedisError, OSError):
        return False


@router.get("/health/live")
def liveness_check() -> dict[str, str]:
    return {"status": "alive"}


@router.get("/health/ready")
def readiness_check() -> dict:
    settings = get_settings()

    checks = {
        "postgres": check_postgres(settings.database_url),
        "neo4j": check_neo4j(
            settings.neo4j_uri,
            settings.neo4j_user,
            settings.neo4j_password.get_secret_value(),
        ),
        "redis": check_redis(settings.redis_url),
    }

    results = {
        name: "ok" if healthy else "unavailable" for name, healthy in checks.items()
    }

    if not all(checks.values()):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "not_ready",
                "checks": results,
            },
        )

    return {
        "status": "ready",
        "checks": results,
    }
