from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
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
    OPENAI_API_KEY: str  = sk-proj-
lsJQif0WlmHUtnKMyKFXuVHHxijxaSJZ9p2KW9RmBnWcGAOvOrKfCAcgmlfen1rlzdHFgRXrM6T3BlbkFJZFMYTvwEAvNXf7QsebACXLGK7KS_2Aqv4aPnwt9KvllKg4FJ1TkwyKLbj2JNtC_WZvgJhn8gUA

    class Config:
        env_file = ".env"

settings = Settings()





















