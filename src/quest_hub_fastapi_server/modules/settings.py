from pydantic import SecretStr
from pydantic_settings import BaseSettings


class EnvirementsSettings(BaseSettings):
    FASTAPI_HOST: str
    FASTAPI_PORT: int
    SUPABASE_URL: str
    SUPABASE_KEY: SecretStr
    BOT_TOKEN : SecretStr

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        validate_default = True


envirements = EnvirementsSettings()


class Fastapi(BaseSettings):
    host: str = envirements.FASTAPI_HOST
    port: int = envirements.FASTAPI_PORT


class Supabase(BaseSettings):
    url: str = envirements.SUPABASE_URL
    key: SecretStr = envirements.SUPABASE_KEY

class TelegramBot(BaseSettings):
    token: SecretStr = envirements.BOT_TOKEN

class EnvSettings(BaseSettings):
    fastapi: Fastapi = Fastapi()
    supabase: Supabase = Supabase()
    telegram_bot: TelegramBot = TelegramBot()


settings = EnvSettings()
