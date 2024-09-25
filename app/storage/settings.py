from pydantic_settings import BaseSettings, SettingsConfigDict


class StorageSettings(BaseSettings):

    SSH_NAME: str
    SSH_PASS: str

    model_config = SettingsConfigDict(env_file=".env")