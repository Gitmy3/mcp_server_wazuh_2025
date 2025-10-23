from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    OPENSEARCH_HOST: str = "http://localhost:9200"
    OPENSEARCH_USER: str  = "Preetam"
    OPENSEARCH_PASS: str  = "wazuh"
    INDEX_ALLOWLIST: List[str] = ["wazuh-alerts-*"]
    FIELD_ALLOWLIST: List[str] = [
        "rule.id", "rule.level", "agent.name",
        "data.srcip", "@timestamp", "manager.name", "vulnerability.severity"
    ]
    TIME_MAX_DAYS: int = 14
    MAX_LIMIT: int = 200
    DEFAULT_TZ: str = "UTC"

    WAZUH_API_HOST: str = "localhost"
    WAZUH_API_PORT: int = 55000
    WAZUH_API_USERNAME: str = "wazuh"
    WAZUH_API_PASSWORD: str = "wazuh"
    WAZUH_INDEXER_HOST: str = "localhost"
    WAZUH_INDEXER_PORT: int = 9200
    WAZUH_INDEXER_USERNAME: str = "admin"
    WAZUH_INDEXER_PASSWORD: str = "admin"
    WAZUH_VERIFY_SSL: bool = False

    # 🧠 Add OpenAI key
    OPENAI_API_KEY: str  = "sk-proj-"
    

    class Config:
        validate_by_name = True  # ✅ Pydantic v2 key
        env_file = ".env"

settings = Settings()






















































