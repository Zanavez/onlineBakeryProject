from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_db: str
    postgres_password: str
    pgport: int


settings = Settings(_env_file="settings_server.env", _env_file_encoding="utf-8")
