from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Config(BaseSettings):
    app_name: str = "FastAPIBackend"
    debug: bool = False
    
    # PostgreSQL configuration from environment variables
    postgres_user: str = "user"
    postgres_password: str = "password"
    postgres_db: str = "test_db"
    postgres_host: str = "localhost"  # Default for local dev
    postgres_port: int = 5432
    
    @property
    def db_url(self) -> str:
        """Build PostgreSQL connection URL from environment variables."""
        return (
            f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


config = Config()
