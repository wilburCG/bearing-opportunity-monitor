from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "行业舆情系统"
    env: str = "dev"
    database_url: str
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "bearing_source_chunks"
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "bearing_neo4j_password"
    gaode_api_key: str | None = None
    llm_provider: str | None = None
    llm_base_url: str | None = None
    llm_api_key: str | None = None
    llm_model: str | None = None
    embedding_model: str | None = None

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
