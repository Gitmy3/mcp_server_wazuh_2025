from pydantic import BaseSettings
from typing import List

class Settings(BaseSettings):
    OPENSEARCH_HOST: str = "http://localhost:9200"
    OPENSEARCH_USER: str | None = None
    OPENSEARCH_PASS: str | None = None
    INDEX_ALLOWLIST: List[str] = ["wazuh-alerts-*"]
    FIELD_ALLOWLIST: List[str] = [
        "rule.id", "rule.level", "agent.name",
        "data.srcip", "@timestamp", "manager.name", "vulnerability.severity"
    ]
    TIME_MAX_DAYS: int = 14
    MAX_LIMIT: int = 200
    DEFAULT_TZ: str = "UTC"

settings = Settings()

