from dotenv import load_dotenv
import os

load_dotenv()


# Database
class Database:
    def __init__(self):
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")
        self.name = os.getenv("DB_NAME")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASS")
        self.async_db_uri = f'postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}'

    @property
    def db_uri(self):
        return self.async_db_uri


class JWT:
    def __init__(self):
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.algorithm = "HS256"
        self.access_token_expire = 60 * 24  # 1 day
        self.refresh_token_expire = 60 * 24 * 7  # 7 days


database = Database()
jwt_config = JWT()
