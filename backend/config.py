from pydantic import BaseSettings


class Settings(BaseSettings):
    ENV: str
    GPU_INFO_DIR: str

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'